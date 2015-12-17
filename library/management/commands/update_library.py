import os
import glob
import json
import logging
from pygithub3 import Github
import pprint

from django.core.management.base import BaseCommand
from library.models import Bundle
from library import github_repo as github
from optparse import make_option

CHANNEL_REPO_OWNER = "kporangehat"
CHANNEL_REPO = "shareshot_channel"
LOCAL_CHANNELS_DIR = "channel_repos"

GITHUB_AUTH_USER = "kporangehat"
GITHUB_AUTH_TOKEN = "27e909305f7b73cc9347d19c990d3b951921c5ab"


class Command(BaseCommand):
    '''
    Django command to update the database with the latest information
    '''
    help = 'Update contributed bundle information'
    logging.basicConfig(level=logging.INFO)  # Make sure we have a basic log handler at hand

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
        gh = Github(user=GITHUB_AUTH_USER, token=GITHUB_AUTH_TOKEN)
        channel_repo = gh.repos.get(user=user, repo=repo)
        logging.info("Loading channel repo data from %s", channel_repo.html_url)

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
            logging.info("Processing channel file %s",  file)
            category = file[:-5]
            with open(file) as fh:
                repo_data[category] = json.load(fh).get("bundles")

        return repo_data

    def load_bundle_metadata(self, bundle_data):
        # locate github repo
        logging.info('Loading bundle metadata from developer\'s site: "%s"', bundle_data.get("name"))
        repo = github.load_repo_url(bundle_data.get("details"))
        metadata = github.get_metadata(repo)
        bundle_data.update(metadata)

    def update_bundle(self, bundle_data):
        logging.info('Updating database for "%s"', bundle_data.get("name"))
        bundle_db_data = Bundle.map_channel_fields_to_db(bundle_data)
        logging.info('%s', pprint.pformat(bundle_db_data))
        obj, created = Bundle.objects.update_or_create(source_url=bundle_db_data["source_url"],
                        defaults=bundle_db_data)
        if created:
            logging.info('Created new record for "%s"', bundle_db_data.get("name"))
        else:
            logging.info('Updated data for "%s"', bundle_db_data.get("name"))

    def update_library(self, channel):
        for category, bundles in channel.iteritems():
            for bundle_data in bundles:
                self.load_bundle_metadata(bundle_data=bundle_data)
                bundle_data["category"] = category
                self.stdout.write(self.style.SUCCESS('Loaded bundle data for "%s"' % bundle_data.get("name")))
                self.update_bundle(bundle_data)






# from django.core.management.base import BaseCommand, CommandError
# from library.models import Bundle
#
# class Command(BaseCommand):
#     help = 'Updates the Library database'
#
#     # def add_arguments(self, parser):
#     #     parser.add_argument('category', nargs='+', type=str)
#
#     def handle(self, *args, **options):
#         for poll_id in options['poll_id']:
#             try:
#                 poll = Poll.objects.get(pk=poll_id)
#             except Poll.DoesNotExist:
#                 raise CommandError('Poll "%s" does not exist' % poll_id)
#
#             poll.opened = False
#             poll.save()
#
#             self.stdout.write(self.style.SUCCESS('Successfully closed poll "%s"' % poll_id))