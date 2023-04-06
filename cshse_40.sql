-- phpMyAdmin SQL Dump
-- version 4.9.7
-- https://www.phpmyadmin.net/
--
-- Хост: localhost
-- Время создания: Апр 06 2023 г., 10:43
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
-- База данных: `cshse_40`
--

-- --------------------------------------------------------

--
-- Структура таблицы `items`
--
-- Создание: Апр 06 2023 г., 05:01
-- Последнее обновление: Апр 06 2023 г., 07:41
--

DROP TABLE IF EXISTS `items`;
CREATE TABLE `items` (
  `item_id` int(10) UNSIGNED NOT NULL,
  `item_name` text COLLATE utf8_unicode_ci NOT NULL,
  `owner_id` int(10) UNSIGNED NOT NULL,
  `item_description` text COLLATE utf8_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Дамп данных таблицы `items`
--

INSERT INTO `items` (`item_id`, `item_name`, `owner_id`, `item_description`) VALUES
(3, 'Пятерка от Андрюши', 0, 'Настоящая пятерка от Андрюши. Правда с учетом минусов');

-- --------------------------------------------------------

--
-- Структура таблицы `items_base`
--
-- Создание: Апр 06 2023 г., 05:02
-- Последнее обновление: Апр 06 2023 г., 07:42
--

DROP TABLE IF EXISTS `items_base`;
CREATE TABLE `items_base` (
  `item_id` int(11) NOT NULL,
  `item_name` text NOT NULL,
  `item_description` text NOT NULL,
  `score` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Дамп данных таблицы `items_base`
--

INSERT INTO `items_base` (`item_id`, `item_name`, `item_description`, `score`) VALUES
(1, 'Яблоко', 'Просто яблоко. Вкусно и негрустно', 40),
(2, 'Банан', 'Настоящий банан! Кожура в подарок', 45),
(3, 'Меч', 'Почти настоящий меч. Достался от деда, а спрашивать у него, откуда меч, уже поздно', 100),
(4, 'Латунный шлем', 'В этой шапке точно не простудишься', 200);

-- --------------------------------------------------------

--
-- Структура таблицы `tasks`
--
-- Создание: Апр 06 2023 г., 05:02
--

DROP TABLE IF EXISTS `tasks`;
CREATE TABLE `tasks` (
  `task_id` int(10) UNSIGNED NOT NULL,
  `user_id` int(10) UNSIGNED NOT NULL,
  `task_title` text COLLATE utf8_unicode_ci NOT NULL,
  `task_description` text COLLATE utf8_unicode_ci NOT NULL,
  `difficulty_level` int(10) UNSIGNED NOT NULL,
  `reward_id` int(10) UNSIGNED NOT NULL,
  `reward_name` text COLLATE utf8_unicode_ci NOT NULL,
  `time_to_complete` bigint(20) NOT NULL,
  `origin_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- --------------------------------------------------------

--
-- Структура таблицы `tasks_base`
--
-- Создание: Апр 06 2023 г., 05:02
-- Последнее обновление: Апр 06 2023 г., 07:42
--

DROP TABLE IF EXISTS `tasks_base`;
CREATE TABLE `tasks_base` (
  `task_id` int(10) UNSIGNED NOT NULL,
  `time_to_complete` bigint(20) UNSIGNED NOT NULL,
  `title` text
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Дамп данных таблицы `tasks_base`
--

INSERT INTO `tasks_base` (`task_id`, `time_to_complete`, `title`) VALUES
(1, 45, 'Слежка за милой бабушкой'),
(2, 90, 'Спасти рядового кота'),
(3, 120, 'Убить 400 слизней'),
(4, 200, 'Потаскать ящики');

-- --------------------------------------------------------

--
-- Структура таблицы `users`
--
-- Создание: Апр 06 2023 г., 05:01
-- Последнее обновление: Апр 06 2023 г., 07:39
--

DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
  `user_id` int(10) UNSIGNED NOT NULL,
  `login` text COLLATE utf8_unicode_ci NOT NULL,
  `pwd_hash` text COLLATE utf8_unicode_ci NOT NULL,
  `score` int(11) NOT NULL,
  `pic_path` text COLLATE utf8_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

--
-- Дамп данных таблицы `users`
--

INSERT INTO `users` (`user_id`, `login`, `pwd_hash`, `score`, `pic_path`) VALUES
(0, 'admin', '8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918', -1, ''),
(1, 'loshara', 'psw', 40, ''),
(2, 'nn', 'sakjfhlksjdf', 10, ''),
(3, '1', '2', 0, ''),
(4, 'noname', 'pwd', 0, '');

--
-- Индексы сохранённых таблиц
--

--
-- Индексы таблицы `items`
--
ALTER TABLE `items`
  ADD PRIMARY KEY (`item_id`),
  ADD KEY `owner_id` (`owner_id`);

--
-- Индексы таблицы `items_base`
--
ALTER TABLE `items_base`
  ADD PRIMARY KEY (`item_id`);

--
-- Индексы таблицы `tasks`
--
ALTER TABLE `tasks`
  ADD PRIMARY KEY (`task_id`),
  ADD UNIQUE KEY `task_id` (`task_id`),
  ADD KEY `reward_id` (`reward_id`),
  ADD KEY `user_id` (`user_id`);

--
-- Индексы таблицы `tasks_base`
--
ALTER TABLE `tasks_base`
  ADD PRIMARY KEY (`task_id`),
  ADD UNIQUE KEY `task_id` (`task_id`);

--
-- Индексы таблицы `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`user_id`);

--
-- AUTO_INCREMENT для сохранённых таблиц
--

--
-- AUTO_INCREMENT для таблицы `items`
--
ALTER TABLE `items`
  MODIFY `item_id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT для таблицы `items_base`
--
ALTER TABLE `items_base`
  MODIFY `item_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT для таблицы `tasks`
--
ALTER TABLE `tasks`
  MODIFY `task_id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=37;

--
-- AUTO_INCREMENT для таблицы `tasks_base`
--
ALTER TABLE `tasks_base`
  MODIFY `task_id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT для таблицы `users`
--
ALTER TABLE `users`
  MODIFY `user_id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- Ограничения внешнего ключа сохраненных таблиц
--

--
-- Ограничения внешнего ключа таблицы `items`
--
ALTER TABLE `items`
  ADD CONSTRAINT `items_ibfk_1` FOREIGN KEY (`owner_id`) REFERENCES `users` (`user_id`);

--
-- Ограничения внешнего ключа таблицы `tasks`
--
ALTER TABLE `tasks`
  ADD CONSTRAINT `tasks_ibfk_1` FOREIGN KEY (`reward_id`) REFERENCES `items` (`item_id`),
  ADD CONSTRAINT `tasks_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
