GET_ALL_COURSES = '''
--получение всех сохраненных данных по валюте
SELECT name, last_price, best_bid_price, best_ask_price, created_at FROM courses c
WHERE
    ($1::varchar IS NULL OR c.name = $1::varchar)
ORDER BY created_at DESC'''

GET_END_COURSES = '''
--получение последнего курса
SELECT name, last_price, best_bid_price, best_ask_price, created_at FROM courses c
WHERE
    ($1::varchar IS NULL OR c.name = $1::varchar)
ORDER BY created_at DESC LIMIT 1'''

GET_RANGE_COURSES = '''
--получение курсов за определенный период
SELECT name, last_price, best_bid_price, best_ask_price, created_at FROM courses c
WHERE
    ($1::varchar IS NULL OR c.name = $1::varchar)
    AND ($2::timestamp IS NULL OR c.created_at >= $2::timestamp)
    AND ($3::timestamp IS NULL OR c.created_at <= $3::timestamp)
'''

ADD_COURSES = '''
--добавление нового курса валюты
INSERT INTO courses (name, last_price, best_bid_price, best_ask_price, created_at) VALUES ($1, $2, $3, $4, $5)'''