MULTI CHAR DELIMITER FOR HIVE USING INPUTFORMAT & OUTPUTFORMAT
=====
    add hive multi char delimeter MULTICHAR_JAR (ex. |@| )
    maybe you can use serde for regex parse your record ,
    but when field having 30 or more field , the serde doesnt work for us.

how to use
====
    - compile to jar
        javac -classpath /usr/lib/hadoop/hadoop-core-1.1.2.21.jar *.java
        jar -cf MULTICHAR.jar *.class

    - add your jar file to your path (ex. /tmp)
      cp MULTICHAR.jar /tmp/
      in hive
      > add jar /tmp/MULTICHAR.jar ;

DDL
====

    CREATE TABLE WEBLOG(
    (
    WEBPAGEID  STRING,
    URL STRING,
    TITLE STRING
    CDATE              DATE
    )
    stored as INPUTFORMAT 'MULTICHARInputFormat'
    OUTPUTFORMAT 'org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat' ;

DATA
====

    1|@|http://www.thu.edu.tw|@|THU|@|20130423
    2|@|http://tw.yahoo.com.tw|@|YAHOO|@|20130426

    aa
