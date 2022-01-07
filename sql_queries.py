from os import curdir
import psycopg2
from psycopg2 import sql
from db import connect

# Returns a list of tuples with the following values:
# (module_code, module_title, year, semester, round, ug)
def latest_round_vacancy(mod_code, number_of_rounds=1, options=['ug']):
   cursor = connect().cursor()
   query = sql.SQL(
      """
      SELECT module_code, year, semester, round, {0} FROM test 
      WHERE module_code={1}
      GROUP BY module_code, semester, year, round
      ORDER BY year DESC, semester DESC, round DESC
      LIMIT {2};
      """
   ).format(
      sql.SQL(', ').join(
         list(map(lambda x: sql.SQL("SUM({}) AS {}").format(sql.SQL(x), sql.SQL(x)), options))),
      sql.Literal(mod_code),
      sql.Literal(number_of_rounds)
   )

   cursor.execute(query)
   return cursor.fetchall()

def past_year_but_same_round_vacancy(mod_code, round, how_far_back=1, options=['ug']):
   cursor = connect().cursor()
   query = sql.SQL(
      """
      SELECT module_code, year, semester, round, {0} FROM test 
      WHERE module_code={1} AND round={2}
      GROUP BY module_code, semester, year, round
      ORDER BY year DESC, semester DESC
      LIMIT {3};
      """
   ).format(
      sql.SQL(', ').join(
         list(map(lambda x: sql.SQL("SUM({}) AS {}").format(sql.SQL(x), sql.SQL(x)), options))),
      sql.Literal(mod_code),
      sql.Literal(round),
      sql.Literal(how_far_back)
   )

   cursor.execute(query)
   return cursor.fetchall()
