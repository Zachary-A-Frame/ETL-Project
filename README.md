# ETL-Project

Data is grabbed from the following sources: 
  Worldbank: https://blogs.worldbank.org/tags/data-news?page=0
  Knoema human development datasets: https://knoema.com/search?query=human%20development&scope=datasets&tab=more
  HDR: http://hdr.undp.org/en/countries
  
  Data encompasses global health articles/ data sets, some of this data displays author data, others do not, some contain subtitle data which can be used for filtering and some do not. Database used will be a relational database. This is because this data is aggregated into a table containing four columns; title, subtitle, author, link. 
  
  The first contains very like-data, and so will scrape from two sources articles that have similar attributes ((id), title, subtitle, author, link), we will have default values for missing information. Some articles contain multiple subtitles. The second table contains GDHI links by country. This is useful, because you can query SQL to respond with only values that relate to a specific country from the first table, and the second table can respond with related (GDHI) datasets, which there should almost always be at least one since it covers every country. 
