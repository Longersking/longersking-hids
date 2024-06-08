-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- 主机： localhost
-- 生成日期： 2024-06-08 20:45:50
-- 服务器版本： 5.7.44-log
-- PHP 版本： 7.4.33

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- 数据库： `hids`
--

-- --------------------------------------------------------

--
-- 表的结构 `events`
--

CREATE TABLE `events` (
  `event_id` int(11) NOT NULL,
  `event_type` varchar(50) NOT NULL,
  `description` text,
  `timestamp` datetime DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- 表的结构 `ip_disabled`
--

CREATE TABLE `ip_disabled` (
  `id` int(11) NOT NULL,
  `ip` varchar(255) DEFAULT NULL COMMENT '被封禁IP',
  `create_time` timestamp NULL DEFAULT NULL COMMENT '添加时间',
  `operator` int(11) DEFAULT NULL COMMENT '操作人'
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COMMENT='IP封禁表';

--
-- 转存表中的数据 `ip_disabled`
--

INSERT INTO `ip_disabled` (`id`, `ip`, `create_time`, `operator`) VALUES
(17, '158.51.120.69', '2024-06-05 11:18:07', 1),
(4, '111.111.111.221', '2024-06-05 08:42:04', 1),
(6, '111.111.111.221', '2024-06-05 08:56:52', 2),
(7, '181.12.158.77', '2024-06-05 09:02:31', 33),
(8, '120.179.51.194', '2024-06-05 09:03:19', 33),
(9, '204.79.37.178', '2024-06-05 09:03:20', 33),
(10, '190.223.212.251', '2024-06-05 09:03:21', 33),
(11, '98.196.4.207', '2024-06-05 09:03:22', 33),
(12, '112.243.203.171', '2024-06-05 09:03:22', 33),
(13, '59.77.122.111', '2024-06-05 09:03:23', 33),
(14, '130.156.163.89', '2024-06-05 09:03:24', 33),
(15, '130.156.163.89', '2024-06-05 09:03:24', 33),
(16, '130.156.163.89', '2024-06-05 09:03:25', 33),
(18, '218.207.122.145', '2024-06-05 11:18:09', 1),
(19, '13.170.10.246', '2024-06-05 11:18:24', 1);

-- --------------------------------------------------------

--
-- 表的结构 `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `username` varchar(50) COLLATE utf8mb4_bin NOT NULL,
  `disabled` int(10) DEFAULT NULL,
  `hashed_password` varchar(100) COLLATE utf8mb4_bin NOT NULL,
  `role` varchar(50) COLLATE utf8mb4_bin DEFAULT NULL,
  `avatar` varchar(1000) COLLATE utf8mb4_bin DEFAULT NULL,
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间'
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin ROW_FORMAT=DYNAMIC;

--
-- 转存表中的数据 `users`
--

INSERT INTO `users` (`id`, `username`, `disabled`, `hashed_password`, `role`, `avatar`, `create_time`) VALUES
(1, 'admin', 0, '$2b$12$0tSZL9MDDwEMf6ZiBdNjpek7dYP1cYkiLHuVCw2iguhcuaFTww8ma', 'admin', '111', '2024-06-05 17:29:50'),
(38, 'abc666', 0, '$2b$12$RJiPSatQ8o1KiSXrNRCWTu2Rq2pR5N3rrNW0PNCovWmXt8nrQbMte', 'user', NULL, NULL),
(36, 'aaa888', 0, '$2b$12$HUialXjlh/M9lw8m5lIhLu9l/7Tn5v3t4LIEQE34FxnQ4OqA/AFzm', 'user', '1111', NULL),
(37, 'askijnhfasd', 0, '$2b$12$aMxv/eRWSDWgq.t0xRLuueS5Gd384RaIcbjFRMIAxl6kW/nUgRxGK', 'user', NULL, NULL),
(35, '5555', 0, '$2b$12$SUfR1/4CC8vr8BAZ2ZNqm.NhE.BDZB88sZlamZgc12k8rHsUgxo4q', 'user', NULL, NULL),
(39, 'abc0000', 0, '$2b$12$uaLHzzFMHKvp95O0lySctOnsiue/kCVQW685GCKvkdOTnrt0o2d72', 'user', NULL, NULL),
(40, 'aaa999', 0, '$2b$12$X3OTdVbwETLsrQuF9RkGIeGLN.DQr9pP0KUvfmfosY7GDrgNrhInO', 'user', NULL, NULL),
(41, 'aaa990', 0, '$2b$12$avcCNKVJX.9zx2saxqTWkefbKpa2E2rgUelrNRDJRTt2Omhla8He6', 'user', NULL, NULL),
(42, 'sdajk', 0, '$2b$12$8g/74w2vo.SchQTGHuNWzO6Jyj14t.u2IGCWTHhyyGGjvLzHkB1GK', 'user', NULL, NULL),
(43, 'root', 0, '$2b$12$MFfvxncD9fNKon7bBiz7LO9ZoXV4unBut8yH4MJF10.I.5ak07A/m', 'admin', NULL, NULL),
(44, 'sys', 0, '$2b$12$ObA8Pkaf4jLH4Z4wUKBctuhoRt4I.M9PrEmHLB4oz5yFcvEdzS2cO', 'admin', NULL, NULL),
(45, 'aaa8888', 0, '$2b$12$8Vxp6Un1XUbso.ZHPcnnFetBgR28IA8tD8ccRyqwFsndV6M0Fr172', 'user', NULL, NULL),
(46, 'asjldja', 0, '$2b$12$/sLz9eIZP5ayCluxbrYZ5e8kGKfER9lqO28S.N91RA8CXswsVbf.C', 'user', NULL, NULL),
(47, 'aaa777', 0, '$2b$12$r/.buCi7wZekOyrx01rkg.IKfQxuWcBgO5Bq1u0gfxM8KLnnlyxJC', 'user', NULL, '2024-06-07 10:39:24');

-- --------------------------------------------------------

--
-- 表的结构 `user_log`
--

CREATE TABLE `user_log` (
  `id` int(11) NOT NULL,
  `uid` int(11) NOT NULL,
  `ip` varchar(50) NOT NULL,
  `username` varchar(50) NOT NULL,
  `login_time` datetime DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 ROW_FORMAT=DYNAMIC;

--
-- 转存表中的数据 `user_log`
--

INSERT INTO `user_log` (`id`, `uid`, `ip`, `username`, `login_time`) VALUES
(1, 1, '127.0.0.1', 'admin', '2024-06-05 10:56:53'),
(2, 1, '192.168.211.26', 'admin', '2024-06-05 11:02:01'),
(3, 1, '192.168.211.125', 'admin', '2024-06-05 11:02:38'),
(4, 1, '192.168.211.26', 'admin', '2024-06-05 11:05:11'),
(5, 1, '192.168.211.125', 'admin', '2024-06-05 11:05:18'),
(6, 1, '127.0.0.1', 'admin', '2024-06-05 11:17:23'),
(7, 1, '127.0.0.1', 'admin', '2024-06-06 16:22:10'),
(8, 1, '127.0.0.1', 'admin', '2024-06-07 02:05:44'),
(9, 1, '127.0.0.1', 'admin', '2024-06-07 02:06:03'),
(10, 2, '88.111.22.34', 'test', '2024-06-07 10:09:03'),
(11, 3, '187.90.11.178', 'aaa111', '2024-06-07 10:09:21'),
(12, 5, '111.78.190.231', 'abc111', '2024-06-07 10:09:37'),
(13, 1, '112.28.229.149', 'admin', '2024-06-08 09:09:53'),
(14, 1, '223.240.142.17', 'admin', '2024-06-08 09:15:25'),
(15, 1, '223.240.142.17', 'admin', '2024-06-08 09:16:12'),
(16, 1, '223.240.142.17', 'admin', '2024-06-08 09:16:12'),
(17, 1, '39.144.38.29', 'admin', '2024-06-08 09:16:23');

--
-- 转储表的索引
--

--
-- 表的索引 `events`
--
ALTER TABLE `events`
  ADD PRIMARY KEY (`event_id`),
  ADD KEY `ix_events_event_id` (`event_id`);

--
-- 表的索引 `ip_disabled`
--
ALTER TABLE `ip_disabled`
  ADD PRIMARY KEY (`id`);

--
-- 表的索引 `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`) USING BTREE,
  ADD UNIQUE KEY `username` (`username`) USING BTREE,
  ADD KEY `ix_users_id` (`id`) USING BTREE;

--
-- 表的索引 `user_log`
--
ALTER TABLE `user_log`
  ADD PRIMARY KEY (`id`) USING BTREE,
  ADD KEY `ix_user_log_id` (`id`) USING BTREE;

--
-- 在导出的表使用AUTO_INCREMENT
--

--
-- 使用表AUTO_INCREMENT `events`
--
ALTER TABLE `events`
  MODIFY `event_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- 使用表AUTO_INCREMENT `ip_disabled`
--
ALTER TABLE `ip_disabled`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;

--
-- 使用表AUTO_INCREMENT `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=48;

--
-- 使用表AUTO_INCREMENT `user_log`
--
ALTER TABLE `user_log`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
