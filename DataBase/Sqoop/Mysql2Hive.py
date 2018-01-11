
sqoop create-hive-table --connect jdbc:mysql://172.16.10.26:3306/xh_elasticsearch --table xhschool_info --username *** --password *** --hive-table xhschool_info

sqoop import --connect jdbc:mysql://172.16.10.26:3306/xh_elasticsearch --username *** --password *** --table xhschool_info --hive-import --hive-table xhschool_info



-incremental lastmodified -check-column created -last-value ‘2012-02-01 11:0:00′
