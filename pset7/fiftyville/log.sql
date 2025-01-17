-- Keep a log of any SQL queries you execute as you solve the mystery.
SELECT description
FROM crime_scene_reports
WHERE year = 2024
AND month = 7
AND day = 28
AND street = 'Humphrey Street';

-- //////////////////
SELECT name, transcript
FROM interviews
WHERE year = 2024
AND month = 7
AND day = 28;

-- ////////////////

SELECT name FROM people
WHERE name = 'Eugen';

-- /////////////////////
SELECT name, transcript
FROM interviews
WHERE year = 2024
AND month = 7
AND day = 28
AND transcript LIKE '%bakery%'
ORDER BY name;

-- /////////////////

SELECT account_number, amount
FROM atm_transactions
WHERE year = 2024
AND month = 7
AND day = 28
AND atm_location = 'Leggett Street'
AND transaction_type = 'withdraw';

-- /////


SELECT name, atm_transactions.amount
FROM people
JOIN bank_accounts
ON people.id = bank_accounts.person_id
JOIN atm_transactions
ON bank_accounts.account_number = atm_transactions.account_number
WHERE atm_transactions.year = 2024
AND atm_transactions.month = 7
AND atm_transactions.day = 28
AND atm_transactions.atm_location = 'Leggett Street'
AND atm_transactions.transaction_type = 'withdraw';

-- ////////////
SELECT abbreviation, full_name, city
FROM airports
WHERE city = 'Fiftyville';

-- ////////////

SELECT flights.id, full_name, city, flights.hour, flights.minute
FROM airports
JOIN flights
ON airports.id = flights.destination_airport_id
WHERE flights.origin_airport_id =
(
    SELECT id
    FROM airports
    WHERE city = 'Fiftyville'
)
AND flights.year = 2024
AND flights.month = 7
AND flights.day = 29
ORDER BY flights.hour, flights.mintue;

-- ////////////////

-- // i see this video in aparat and continue other query https://www.aparat.com/v/k55z533
