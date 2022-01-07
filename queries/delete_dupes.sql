DELETE FROM test
WHERE ctid NOT IN (
   SELECT min(ctid)                   
   FROM test
   GROUP BY faculty_school, department, module_code, 
   module_title, module_class, ug, gd,dk,ng,cpe,year,semester,round);