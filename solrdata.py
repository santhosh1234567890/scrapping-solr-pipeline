import json

import requests

import config as config


class SolrResponse:

    # Constructor
    # Input parameters
    # 1. keyword = User request keyword to fetch documents
    # 2. content_type_response = Type of content in which document should be fetched
    # 3. num_doc = User requested Number of documents
    def __init__(self, keyword, content_type_response, num_doc):
        self.keyword = keyword
        self.content_type_response = content_type_response

        # check whether the document count is specified or not
        # if it is not specified then set num_doc to the value from config file
        self.num_doc = config.doc_count if num_doc == "" else num_doc

        # variables to store Solr Json in specific format
        self.content_pdf = []  # List to store pdf details
        self.content_text = []  # List to store text details
        self.content_videos = []  # List to store video details
        self.content_program = []  # List to store program details
        self.final_out_multi = []  # List to append documents details of multi content type

    # solr_data --> to split required data from solr response and store it in a variable
    def solr_data(self):
        # url - request solr to send documents with specified keyword along with necessary details
        base_url = config.solr["base_url"]  # base url
        query_string_parameters = config.solr["query_string_parameters"]  # query string parameters
        url = base_url + self.keyword + query_string_parameters  # Solr url to fetch documents from it
        response = requests.get(url)
        response_json = response.json()  # Json response from Solr
        # Solr returns response in Json format
        # Parse it and fetch our necessary details from that save it in variables
        # doc_count_solr = response_json['responseHeader']['params']['rows']  # Count of documents from Solr
        docs_details = response_json['response']['docs']  # List in which documents
        # print(len(docs_details))
        # print(docs_details[172])
        if len(docs_details) != 0:
            for solr_response in range(len(docs_details)):  # for loop to fetch documents from Solr response
                doc_name = docs_details[solr_response]['doc_name']  # Document name from Solr response
                url = docs_details[solr_response]['path']  # Url of that respective document from Solr response
                url_final = "http://" + config.IP + url[0]
                content_type = docs_details[solr_response]['content_type']  # Type of document from Solr response
                date = docs_details[solr_response]['date']  # Document downloaded date
                score = docs_details[solr_response]['score']  # Score of the respective document
                title = docs_details[solr_response]['title']  # Title of the respective document
                tag_details = docs_details[solr_response]['tag_details']  # Tag_details of the respective document
                doc_id = docs_details[solr_response]['id']
                date_final = round(date[0])  # Solr returns date in decimal " .0" format, so round off the date
                data_parameters = {  # Store the details of documents in a variable
                    'document_name': doc_name[0],
                    'url': url_final,
                    'title': title[0],
                    'content_type': content_type[0],
                    'date': date_final,
                    'score': score,
                    #'tag_details': tag_details,
                    'id': doc_id
                }
                # Check the content type of documents then append it to their respective list
                if content_type[0] == 'pdf':
                    self.content_pdf.append(data_parameters)
                elif content_type[0] == 'videos':
                    self.content_videos.append(data_parameters)
                elif content_type[0] == 'text':
                    self.content_text.append(data_parameters)
                else:
                    self.content_program.append(data_parameters)

    # solr_data_collection --> add the solr response details into their respective lists. Then sort them into
    # descending order and return the top most documents
    # Input parameter - content_file_format --> content_type from respective functions
    def solr_data_collection(self, content_file_format):
        final_out = []  # List to store top most documents
        file_name = 'content_' + content_file_format  # name of list with respective content_type
        content_file = getattr(self, file_name)  # use getattr to get lists from constructor
        len_file = str(len(content_file))
        # print(len_file)
        if len(content_file) > 0:  # If content_text list contains more than one document
            # then sort it in descending order and save it in text_out
            file_name = sorted(content_file, key=lambda item: item['score'], reverse=True)
            # finally append it into final_out list)
            final_out.append(file_name[0:int(self.num_doc)])
            return {'len_content': len_file, 'final_out': final_out}  # return the final data in a list
        else:
            return {'len_content': len_file, 'final_out': [["No Documents Found"]]}

    # doc_response --> store content_type in a list and call solr_data_collection function to get solr json response
    # then return it to rAPI
    @property
    def doc_response(self):
        self.solr_data()  # get solr response from solr_data
        result = {'content_type': {}}
        document_format = ["pdf", "videos", "text", "program"]  # content_type list
        # get the index for user requested content_type from list
        content_type_integer = document_format.index(self.content_type_response)
        # fetch the name of content_type from list
        content_format_file = document_format[content_type_integer]
        final_data = self.solr_data_collection(content_format_file)  # get output data from solr_data_collection
        # result['summary'] = final_data['len_content']
        result = {'content_type': {content_format_file: {}}}
        result['content_type'][content_format_file]['available_documents'] = final_data['len_content']
        if final_data['final_out'][0][0] == 'No Documents Found':
            result['content_type'][content_format_file]['retrieved_documents'] = "0"
        else:
            result['content_type'][content_format_file]['retrieved_documents'] = str(len(final_data['final_out'][0]))
        result['content_type'][content_format_file]['documents'] = final_data['final_out'][0]
         # function, content_format_file is the name of the file format pass to the function to get it's respective data
        return result  # return the final data in a dict

    # doc_response_multi --> content_type is multi then store all content_type in a list and call
    # solr_data_collection in a for loop to get all content_type documents then return it to rAPI
    @property
    def doc_response_multi(self):
        len_document = []
        # result = {'content_type': {content_format_file: {}}}
        self.solr_data()  # call solr_data function
        # this function is for content type multi then call all format functions
        document_format = ["pdf", "videos", "text", "program"]
        result = {'content_type': {'pdf': {}, 'videos': {}, 'text': {}, 'program':{}}}
        for types in range(len(document_format)):
            final_data_solr = []
            final_data_multi = self.solr_data_collection(document_format[types])
            final_data_solr.append(final_data_multi['final_out'][0])
            len_document.append((final_data_multi['len_content']))
            result['content_type'][document_format[types]]['available_documents'] = len_document[types]
            if final_data_solr[0][0] == 'No Documents Found':
                result['content_type'][document_format[types]]['retrieved_documents'] = "0"
            else:
                result['content_type'][document_format[types]]['retrieved_documents'] = str(len(final_data_solr[0]))
                result['content_type'][document_format[types]]['documents'] = final_data_solr[0]
        return result  # return the final data in a dict
