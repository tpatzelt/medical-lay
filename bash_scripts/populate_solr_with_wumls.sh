#NAME="wumls-multi-valued"
#bin/solr create -c $NAME
#curl --request POST   --url http://localhost:8983/api/collections/$NAME/schema   --header 'Content-Type: application/json'   --data '{
#  "add-field": [
#    {"name": "cui", "type": "string", "multiValued": false, "indexed": false},
#    {"name": "source", "type": "string", "multiValued": false, "indexed": false},
#    {"name": "language", "type": "string", "multiValued": false, "indexed": false},
#    {"name": "names", "type": "text_general", "multiValued": true, "indexed": false},
#    {"name": "index_terms", "type": "string", "multiValued": true},
#  ]
#}'
#bin/post -c $NAME ../WUMLS/wumls_index_terms_multi_valued.json 

#NAME="wumls-single-valued"
#bin/solr create -c $NAME
#curl --request POST   --url http://localhost:8983/api/collections/$NAME/schema   --header 'Content-Type: application/json'   --data '{
#  "add-field": [
#    {"name": "cui", "type": "string", "multiValued": false, "indexed": false},
#    {"name": "source", "type": "string", "multiValued": false, "indexed": false},
#    {"name": "language", "type": "string", "multiValued": false, "indexed": false},
#    {"name": "name", "type": "text_general", "multiValued": false, "indexed": false},
#    {"name": "index_term", "type": "string", "multiValued": false},
#  ]
#}'
#bin/post -c $NAME ../WUMLS/wumls_index_terms_single_valued.json 

NAME="wumls-single-valued-deduplicated"
bin/solr create -c $NAME
#bin/solr config -c wumls-single-valued-deduplicated -p 8983 -action set-user-property -property update.autoCreateFields -value false
curl --request POST   --url http://localhost:8983/api/collections/$NAME/schema   --header 'Content-Type: application/json'   --data '{
  "add-field": [
    {"name": "cui", "type": "string", "multiValued": false, "indexed": false},
    {"name": "source", "type": "string", "multiValued": false, "indexed": false},
    {"name": "language", "type": "string", "multiValued": false, "indexed": false},
    {"name": "name", "type": "text_general", "multiValued": false, "indexed": false},
    {"name": "index_term", "type": "string", "multiValued": false},
    {"name": "id", "type": "int", "multiValued": false, "indexed": false},
  ]
}'
bin/post -c $NAME ../WUMLS/wumls_index_terms_single_valued_deduplicated.json 
#
#
#NAME="wumls-single-doc-valued"
#bin/solr create -c $NAME
#curl --request POST   --url http://localhost:8983/api/collections/$NAME/schema   --header 'Content-Type: application/json'   --data '{
#  "add-field": [
#    {"name": "cui", "type": "string", "multiValued": false, "indexed": false},
#    {"name": "source", "type": "string", "multiValued": false, "indexed": false},
#    {"name": "language", "type": "string", "multiValued": false, "indexed": false},
#    {"name": "name", "type": "text_general", "multiValued": false, "indexed": false},
#    {"name": "index_term", "type": "string", "multiValued": false},
#    {"name": "id", "type": "int", "multiValued": false, "indexed": false},
#  ]
#}'
#bin/post -c $NAME ../WUMLS/wumls_index_terms_single_doc_valued.json 