import os
import glob
import json
import logging
from pygithub3 import Github
import pprint

from django.core.management.base import BaseCommand
from library.models import Bundle
from library.models import Release
from library import github_repo as github
from optparse import make_option

CHANNEL_REPO_OWNER = "kporangehat"
CHANNEL_REPO = "shareshot_channel"
LOCAL_CHANNELS_DIR = "channel_repos"

logging.basicConfig(level=logging.INFO)  # Make sure we have a basic log handler at hand
logger = logging.getLogger("library.update_library")


class Command(BaseCommand):
    '''
    Django command to update the database with the latest information
    '''
    help = 'Update contributed bundle information'

    option_list = BaseCommand.option_list + (
        make_option(
            '--update',
            action='store_true',
            dest='update',
            default=False,
            help='Update contributed bundle information'),
    )

    def __init__(self, *args, **kwargs):
        super(Command,self).__init__(*args, **kwargs)

    def handle(self, *args, **options):
        '''
        Command handler, retrieve options and call corresponding methods
        '''
        # Retrieve any loop that was given on the command line
        if options.get('update'):
            # If we had multiple channels to load from this would work fine.
            channel_data = self.load_channel_repo(user=CHANNEL_REPO_OWNER, repo=CHANNEL_REPO)
            self.update_library(channel_data)
        else:
            raise NotImplementedError("Invalid options given %s" % str(options))

    def load_channel_repo(self, user, repo):
        """
        Pulls down the latest updates from the channel repo and loads them.
        :param repo_dict: dictionary with 'user' and 'repo' keys to construct the github repo
        :return:
        """
        # clone repo
        gh = Github(user=github.GITHUB_AUTH_USER, token=github.GITHUB_AUTH_TOKEN)
        channel_repo = gh.repos.get(user=user, repo=repo)
        logger.info("Loading channel repo data from %s", channel_repo.html_url)

        # create channels directory (safely)
        try:
            os.makedirs("channel_repos")
        except OSError:
            pass

        # enter channels dir
        os.chdir("channel_repos")

        # git pull if we already have it
        if os.path.exists(channel_repo.name):
            os.chdir(channel_repo.name)
            os.system('git pull')
            os.chdir("..")
        # create dir and git clone if we don't
        else:
            os.system('git clone %s' % channel_repo.clone_url)

        os.chdir("%s/repository" % channel_repo.name)
        repo_data = {}
        for file in glob.glob("*.json"):
            logger.info("Processing channel file %s",  file)
            category = file[:-5]
            with open(file) as fh:
                repo_data[category] = json.load(fh).get("bundles")

        return repo_data

    def load_bundle_metadata(self, bundle_data):
        # locate github repo
        logger.info('Loading bundle metadata from developer\'s site: "%s"', bundle_data.get("name"))
        repo = github.load_repo_url(bundle_data.get("details"))
        metadata = github.get_metadata(repo)
        bundle_data.update(metadata)

    def update_bundle(self, bundle_data):
        logger.info('Updating database for "%s"', bundle_data.get("name"))
        bundle_db_data = Bundle.map_channel_fields_to_db(bundle_data)
        logger.info('%s', pprint.pformat(bundle_db_data))
        bundle, created = Bundle.objects.update_or_create(source_url=bundle_db_data["source_url"],
                        defaults=bundle_db_data)
        if created:
            logger.info('Created new record for "%s"', bundle_db_data.get("name"))
        else:
            logger.info('Updated data for "%s"', bundle_db_data.get("name"))

        return bundle

    def update_versions(self, bundle_data, bundle):
        logger.info('Updating releases for "%s"', bundle_data.get("name"))
        # look for releases in tags unless a branch is specified
        release_type = bundle_data["releases"][0].get("branch", "tags")
        versions = github.load_versions(bundle.source_url, release_type)
        self.stdout.write(self.style.SUCCESS('Loaded versions from "%s"' % release_type))
        logger.info(versions)
        for v in versions:
            release_db_data = Release.map_version_fields_to_db(bundle, v)
            logger.info('%s', pprint.pformat(release_db_data))
            release, created = Release.objects.update_or_create(bundle=bundle,
                                                                version=release_db_data["version"],
                                                                date=release_db_data["date"],
                                                                defaults=release_db_data)
            if created:
                logger.info('Created new release for "%s"', release_db_data.get("version"))
            else:
                logger.info('Updated release for "%s"', release_db_data.get("version"))


    def update_library(self, channel):
        for category, bundles in channel.iteritems():
            for bundle_data in bundles:
                self.load_bundle_metadata(bundle_data=bundle_data)
                bundle_data["category"] = category
                self.stdout.write(self.style.SUCCESS('Loaded bundle data for "%s"' % bundle_data.get("name")))
                bundle = self.update_bundle(bundle_data)
                self.update_versions(bundle_data, bundle)

