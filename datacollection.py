from solrdata import SolrResponse


def data_collection(keyword, content_type, doc_count):
    # data_collection function calls class from json_response
    # Input parameters
    # 1. keyword = User request keyword to fetch documents
    # 2. content_type_response = Type of content in which document should be fetched
    # 3. num_doc = User requested Number of documents

    # create class instance and call the class
    class_instance = SolrResponse(keyword, content_type, doc_count)

    # check whether content_type is specified or not... if it is specified call the appropriate function
    # and return the Json response
    if content_type == "" or content_type == "multi":
        result = class_instance.doc_response_multi
    else:
        result = class_instance.doc_response
    return result
