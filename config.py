import configparser

config = configparser.ConfigParser()

# number of documents when count of document is not specified in request
doc_count = 5

# IP for documents path
IP = "52.53.165.238"

# url to fetch documents from Solr
solr = {
    "base_url": "http://52.53.165.238:8983"  # base url
                "/solr/documents/select"
                "?q=doc_content:",
    "query_string_parameters": "&fl=doc_name,date,path,content_type,score,tag_details,title,id&wt=json&rows=1000"
    # query string parameters
}
