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
      SELECT module_code, module_title, year, semester, round, {0} FROM test 
      WHERE module_code={1}
      GROUP BY module_code, module_title, semester, year, round
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
      SELECT module_code, module_title,year, semester, round, {0} FROM test 
      WHERE module_code={1} AND round={2}
      GROUP BY module_code, module_title, semester, year, round
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

def reply_message(*args):
   print(args)
   year = args[2]
   semester = args[3]
   round = args[4]
   vacancy = args[5]

   return '{0} Sem{1} R{2}: {3}\n'.format(year_to_AY(year), semester, round, vacancy)

def year_to_AY(year):
   year = year % 100
   next_year = year + 1

   return 'AY{0}/{1}'.format(year, next_year)

def handle_message(mod_code, rounds=1):
   xs = latest_round_vacancy(mod_code, rounds)
   message = "Here are the vacancies for {0}:\n".format(mod_code)

   for tup in xs:
      tup_str = reply_message(*tup)
      message = message + tup_str
   
   return message
      
print(handle_message('ACC1701X', 3))
