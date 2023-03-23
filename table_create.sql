-- phpMyAdmin SQL Dump
-- version 4.9.7
-- https://www.phpmyadmin.net/
--
-- Хост: localhost
-- Время создания: Мар 05 2021 г., 11:56
-- Версия сервера: 5.7.21-20-beget-5.7.21-20-1-log
-- Версия PHP: 5.6.40

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- База данных: `cshse_test_flask`
--

-- --------------------------------------------------------

--
-- Структура таблицы `user`
--

DROP TABLE IF EXISTS 'users';
CREATE TABLE users (
  'user_id' int(4294967295) PRIMARY KEY UNSIGNED AUTO_INCREMENT NOT NULL,
  'login' text COLLATE utf8_unicode_ci NOT NULL,
  'pwd_hash' text(255) COLLATE utf8_unicode_ci NOT NULL,
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Структура таблицы `items`
--

DROP TABLE IF EXISTS 'items';
CREATE TABLE items (
  'item_id' int(4294967295) PRIMARY KEY UNSIGNED AUTO_INCREMENT NOT NULL,
  'item_name' text COLLATE utf8_unicode_ci NOT NULL,
  'owner_id' int(4294967295) UNSIGNED DEFAULT NULL,
  'item_description' text COLLATE utf8_unicode_ci NOT NULL
  FOREIGN KEY ('owner_id') REFERENCES 'users' ('user_id')  
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;


-- --------------------------------------------------------

--
-- Структура таблицы `user`
--

DROP TABLE IF EXISTS 'tasks';
CREATE TABLE 'tasks' (
  'user_id' int(4294967295) UNSIGNED DEFAULT NULL, 
  
  'task_id' int(4294967295) PRIMARY KEY UNSIGNED AUTO_INCREMENT NOT NULL,
  
  'task_title' text COLLATE utf8_unicode_ci NOT NULL,
  'task_description' text COLLATE utf8_unicode_ci NOT NULL,
  'difficulty_level' int(5) UNSIGNED NOT NULL,
  'picture_path' text COLLATE utf8_unicode_ci NOT NULL,
  'time_to_complete' time NOT NULL,

  'reward_id' int(4294967295) PRIMARY KEY UNSIGNED NOT NULL,
  'reward_name' text  COLLATE utf8_unicode_ci NOT NULL,
  FOREIGN KEY ('reward_id') REFERENCES 'items' ('item_id'),
  FOREIGN KEY ('user_id') REFERENCES 'users' ('user_id'),
  FOREIGN KEY ('reward_name') REFERENCES 'items' ('item_name')
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------
-- --------------------------------------------------------
-- --------------------------------------------------------

--
-- Дамп данных таблицы `user`
--

-- INSERT INTO `user` (`id`, `name`, `email`, `image`) VALUES
-- (1, 'Вася ', 'vasya@gmail.com', 'user2.jpg'),
-- (2, 'Маша', 'masha@mail.ru', 'user1.jpg'),
-- (3, 'Петя', 'petya@yandex.ru', 'user3.jpg');

-- COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
