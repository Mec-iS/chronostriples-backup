import webapp2
import datetime

from config.config import _DEBUG
from datastore.models import WebResource

__author__ = 'Lorenzo'


class Indexing(webapp2.RequestHandler):
    """
    A very basic crawler for RSS links
    #TO-DO: implement memecache for stored items not yet indexed
    """

    def get(self):
        """
        Handler for the cronjob: /cron/indexing
        It store keywords indexing of the most recent WebResource stored
        :return:
        """
        # create the Index entries
        from flankers.long_task import storeIndexer
        an_hour = datetime.datetime.now() - datetime.timedelta(hours=1)
        print an_hour
        query = WebResource.query().filter(WebResource.stored > an_hour)
        print query.count()
        for q in query:
            s = storeIndexer()
            s.execute_task(q, q.key)
            del s


application = webapp2.WSGIApplication([
    webapp2.Route('/cron/indexing', Indexing),
], debug=_DEBUG)

