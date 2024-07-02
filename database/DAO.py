from database.DB_connect import DBConnect
from model.stato import Stato


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def get_anni():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct(year(s.`datetime`)) as d
                    from sighting s 
                    order by d"""

        cursor.execute(query)

        for row in cursor:
            result.append(row["d"])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_forme():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct s.shape as sh
                    from sighting s 
                    order by sh"""

        cursor.execute(query)

        for row in cursor:
            result.append(row["sh"])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_vertici():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select *
                    from state s 
                         """

        cursor.execute(query)

        for row in cursor:
            result.append(Stato(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_archi(anno, forma):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select n.state1 as s1, n.state2 as s2, count(*) as peso 
                    from neighbor n, (select * from sighting s where shape = %s and year(s.`datetime`) = %s) as s 
                    where n.state1 > n.state2 and (n.state1 = s.state or n.state2 = s.state)
                    group by n.state1, n.state2 
                    """

        cursor.execute(query, (forma, anno, ))

        for row in cursor:
            result.append([row["s1"], row["s2"], row["peso"]])

        cursor.close()
        conn.close()
        return result

