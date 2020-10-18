from googlesearch import search
from logging import getLogger

logger = getLogger(__name__)


class Search:

    @classmethod
    def search(cls, query, num=5, tld="co.in"):
        """
		Function used to retrieve google query results.
		"""
        try:
            # searching for query on google search.
            result = search(query, tld=tld, num=5, stop=5, pause=2)
            result_string = ""
            count = 1
            for each in result:
                result_string = result_string + str(count) + ". " + each + "\n "
                count += 1
            return result_string
        except Exception as e:
            logger.error(
                "GoogleSearch: search: error found for query:{} with error_details: {}".format(query, str(e)))
            raise e
