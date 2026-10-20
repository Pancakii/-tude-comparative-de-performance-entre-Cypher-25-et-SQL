#Using data generated as in https://www.alibabacloud.com/blog/postgresql-recursive-query-examples-of-depth-first-and-breadth-first-search_599373

#Disclaimer : for termination better bound the number of iterations ! Risks of saturating the memory of your computer are very real.
#In case you forget to bound the depth, you can run that radical emergency query in another terminal to kill everything : 
SELECT pg_cancel_backend(pid)
FROM pg_stat_activity
WHERE state = 'active' and pid <> pg_backend_pid(); 
#cf https://www.sqlprostudio.com/blog/8-killing-cancelling-a-long-running-postgres-query



# Arrays are considered as non ordered structures, as far as containement goes
#ameliegheerbrant=# select  array[array[0,9]] @> array[9,0];
# ?column? 
#----------
# t
#(1 row)
#Works also for array of non integers
#ameliegheerbrant=# select  array[array['9','0']] @> array['0','9'];
# ?column? 
#----------
# t
#(1 row)
#check https://www.postgresql.org/docs/9.1/functions-array.html



# Trails from 1 to 10 (here bounded to depth 9 to allow for the computation) :


with recursive tmp as (                                                                       
select uid, lkuid, 0 as depth, array[uid,lkuid] as path, array[uid||'.'|| lkuid] as edges, lkuid=10 as reached from bs where uid=1  
union all                                                                          
select bs.uid, bs.lkuid, tmp.depth+1, tmp.path||bs.lkuid, tmp.edges || concat(bs.uid||'.',bs.lkuid), bs.lkuid=10   
  from bs , tmp    
  where not tmp.reached and bs.uid=tmp.lkuid   
  and not tmp.edges  @> array[concat(bs.uid||'.',bs.lkuid)] and depth<9
)     
select * from tmp where reached order by depth, path;



# without depth <9 : ERROR:  could not write to file "base/pgsql_tmp/pgsql_tmp39466.224": No space left on device
# Note on edges 9.6 versus 6.9 : they are different edges whenever edges are directed, in the undirected case
# things would be different
# Beware of cases such as 6||11=61||1. Hence the '.' separator.


#Equivalently, using ANY instead of @> :

with recursive tmp as (                                                                       
select uid, lkuid, 0 as depth, array[uid,lkuid] as path, array[uid||'.'|| lkuid] as edges, lkuid=10 as reached from bs where uid=1  
union all                                                                          
select bs.uid, bs.lkuid, tmp.depth+1, tmp.path||bs.lkuid, tmp.edges || concat(bs.uid||'.',bs.lkuid), bs.lkuid=10   
  from bs , tmp    
  where not tmp.reached and bs.uid=tmp.lkuid   
  and not concat(bs.uid||'.',bs.lkuid)=any(tmp.edges) and depth <9
)     
select * from tmp where reached order by depth, path;

##maybe more efficient if we don't keep two different arrays?
# Alternatively we could keep only the simpler path array and use a NOT EXISTS() statement to replace the condition in the WHERE
# introduced by NOT
# We could use WITH ORDINALITY ORDINALITY and UNNEST to access array elements see https://stackoverflow.com/questions/8760419/postgresql-unnest-with-element-number
#It looks a bit cumbersome, especially given syntactic restrictions in recursives CTE, maybe better to generate path from edges
#in the final SELECT clause, TODO : adapt the following query by replacing SELECT * by something more involved

with recursive tmp as (                                                                       
select uid, lkuid, 0 as depth, array[uid||'.'|| lkuid] as edges, lkuid=10 as reached from bs where uid=1  
union all                                                                          
select bs.uid, bs.lkuid, tmp.depth+1, tmp.edges || concat(bs.uid||'.',bs.lkuid), bs.lkuid=10   
  from bs , tmp    
  where not tmp.reached and bs.uid=tmp.lkuid   
  and not tmp.edges  @> array[concat(bs.uid||'.',bs.lkuid)] and depth <9
)     
select * from tmp where reached order by depth, edges;


# Compare with simple paths from 1 to 10 (no need to bound the depth here)


 with recursive tmp as (  
select uid, lkuid, 0 as depth, array[uid,lkuid] as path, lkuid=10 as reached from bs where uid=1   
union all  
select bs.uid, bs.lkuid, tmp.depth+1, tmp.path||bs.lkuid, bs.lkuid=10  
  from bs , tmp    
  where bs.uid=tmp.lkuid   
  and not bs.lkuid=any(tmp.path) and not reached 
)      
select * from tmp where reached order by depth, path;

#Prerequisit on window functions : https://learnsql.com/blog/sql-window-functions-rows-clause/
#And on the aggregate bool_or function : https://www.sqliz.com/postgresql-ref/bool_or/ 
#OK, now let's think about shortest path from 1 to 10 :

WITH RECURSIVE paths(endp, path, level, endReached) AS (
SELECT lkuid AS endp, ARRAY[uid, lkuid] AS path, 1 AS level,
bool_or(CASE WHEN lkuid = 10 THEN true ELSE false END) OVER (ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED
FOLLOWING) AS endReached
FROM bs
WHERE uid = 1
UNION ALL
SELECT bs.lkuid AS endp,
array_append(path, bs.lkuid) AS path, level + 1 AS level,
bool_or(CASE WHEN bs.lkuid = 10 THEN true ELSE false END) OVER (ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED
FOLLOWING) AS endReached
FROM paths JOIN bs ON paths.endp = bs.uid
WHERE lkuid != ALL(paths.path) AND NOT paths.endReached
)
SELECT path, level
FROM paths
WHERE endp = 10;

# There is a direct path in my dataset and the result is as expected :
#  path  | level 
#--------+-------
# {1,10} |     1
#(1 row)


#Now from 1 to 7 :

WITH RECURSIVE paths(endp, path, level, endReached) AS (
SELECT lkuid AS endp, ARRAY[uid, lkuid] AS path, 1 AS level,
bool_or(CASE WHEN lkuid = 7 THEN true ELSE false END) OVER (ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED
FOLLOWING) AS endReached
FROM bs
WHERE uid = 1
UNION ALL
SELECT bs.lkuid AS endp,
array_append(path, bs.lkuid) AS path, level + 1 AS level,
bool_or(CASE WHEN bs.lkuid = 7 THEN true ELSE false END) OVER (ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED
FOLLOWING) AS endReached
FROM paths JOIN bs ON paths.endp = bs.uid
WHERE lkuid != ALL(paths.path) AND NOT paths.endReached
)
SELECT path, level
FROM paths
WHERE endp = 7;

#A bit more interesting in my data set :
#  path   | level 
#---------+-------
# {1,8,7} |     2
# {1,2,7} |     2
# {1,5,7} |     2
# {1,6,7} |     2
#(4 rows)





