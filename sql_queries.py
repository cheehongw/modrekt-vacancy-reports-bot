from os import curdir
import psycopg2
from psycopg2 import sql
from db import connect

# Returns a list of tuples with the following values:
# (module_code, year, semester, round, ug)
def latest_round_vacancy(mod_code, options=['ug']):
   cursor = connect().cursor()
   query = sql.SQL(
      """
      SELECT module_code, year, semester, round, {0} FROM test 
      WHERE module_code={1}
      GROUP BY module_code, semester, year, round
      ORDER BY year DESC, semester DESC, round DESC
      LIMIT 1;
      """
   ).format(
      sql.SQL(', ')
         .join(
            list(map(lambda x: sql.SQL("SUM({}) AS {}").format(sql.SQL(x), sql.SQL(x)), options))),
      sql.Literal(mod_code)
   )

   cursor.execute(query)
   return cursor.fetchall()

print(latest_round_vacancy("CS2100"))
