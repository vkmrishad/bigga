FROM solr:6.6.6
RUN precreate-core core1
RUN rm -rf /opt/solr/server/solr/mycores/core1/conf/managed-scehma
RUN rm -rf /opt/solr/server/solr/configsets/basic_configs/conf/managed-schema
COPY managed-schema /opt/solr/server/solr/configsets/basic_configs/conf/
COPY managed-schema /opt/solr/server/solr/mycores/core1/conf/ 
COPY schema.xml /opt/solr/server/solr/mycores/core1/conf/

