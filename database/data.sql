-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- 主机： localhost
-- 生成日期： 2024-08-12 00:26:17
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
-- 表的结构 `alert_log`
--

CREATE TABLE `alert_log` (
  `id` int(11) NOT NULL,
  `type` varchar(255) DEFAULT NULL COMMENT '告警类型',
  `level` varchar(255) DEFAULT NULL COMMENT '告警等级',
  `ip` varchar(255) DEFAULT NULL COMMENT '主机IP',
  `desc` varchar(1000) DEFAULT NULL COMMENT '告警描述',
  `application` varchar(1000) DEFAULT NULL COMMENT '告警应用',
  `snapshot` text COMMENT '系统快照',
  `source_ip` varchar(255) DEFAULT NULL COMMENT '来源IP',
  `port` varchar(255) DEFAULT NULL COMMENT '来源端口',
  `target_ip` varchar(255) DEFAULT NULL COMMENT '目标IP',
  `target_port` varchar(100) DEFAULT NULL COMMENT '目标端口',
  `packet` text COMMENT '数据包',
  `create_time` datetime DEFAULT NULL COMMENT '告警时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='主机告警表';

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
-- 表的结构 `file_log`
--

CREATE TABLE `file_log` (
  `id` int(11) NOT NULL,
  `ip` varchar(255) DEFAULT NULL COMMENT '主机IP',
  `file_path` varchar(1000) DEFAULT NULL COMMENT '文件路径',
  `action` varchar(1000) DEFAULT NULL COMMENT '变更类型',
  `is_dir` int(10) DEFAULT NULL COMMENT '是否为目录',
  `size` double DEFAULT NULL COMMENT '文件尺寸',
  `owner` varchar(255) DEFAULT NULL COMMENT '所属者',
  `desc` varchar(1000) DEFAULT NULL COMMENT '描述',
  `is_alarms` int(11) DEFAULT NULL COMMENT '是否为警告',
  `content` longtext COMMENT '文件内容',
  `file_create_time` datetime DEFAULT NULL COMMENT '文件创建时间',
  `file_modify_time` datetime DEFAULT NULL COMMENT '文件操作时间',
  `update_time` datetime DEFAULT NULL COMMENT '上次修改时间',
  `log_time` datetime DEFAULT NULL COMMENT '记录即使'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='文件记录表';

-- --------------------------------------------------------

--
-- 表的结构 `hack_ip`
--

CREATE TABLE `hack_ip` (
  `hack_id` int(11) NOT NULL,
  `hack_ip` varchar(50) NOT NULL,
  `description` text,
  `timestamp` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- 表的结构 `host_list`
--

CREATE TABLE `host_list` (
  `host_id` int(11) NOT NULL,
  `host_ip` varchar(45) NOT NULL,
  `operating_system` varchar(100) NOT NULL,
  `alias` varchar(100) DEFAULT NULL,
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `status` varchar(20) DEFAULT 'offline',
  `cpu_cores` int(11) DEFAULT NULL,
  `total_memory_gb` decimal(10,2) DEFAULT NULL,
  `total_disk_space_gb` decimal(10,2) DEFAULT NULL,
  `network_bandwidth_mbps` decimal(10,2) DEFAULT NULL,
  `last_update` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `notes` text
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- 转存表中的数据 `host_list`
--

INSERT INTO `host_list` (`host_id`, `host_ip`, `operating_system`, `alias`, `create_time`, `status`, `cpu_cores`, `total_memory_gb`, `total_disk_space_gb`, `network_bandwidth_mbps`, `last_update`, `notes`) VALUES
(1, '49.232.245.103', 'Centos7.9', '小杜的服务器', '2024-08-04 12:40:43', 'online', 2, '4.00', '50.00', '3.00', '2024-08-04 12:43:27', '无'),
(3, '121.43.138.234', 'Centos7.9', '中控服务器', '2024-08-04 18:01:27', 'online', 8, '16.00', '200.00', '100.00', '2024-08-08 06:38:50', '用于建设服务端的中控服务器'),
(4, '121.43.132.126', 'Centos', '欢喜家的', '2024-08-05 10:45:57', 'online', 8, '8.00', '500.00', '100.00', '2024-08-08 06:38:50', NULL);

-- --------------------------------------------------------

--
-- 表的结构 `ip_disabled`
--

CREATE TABLE `ip_disabled` (
  `id` int(11) NOT NULL,
  `host_ip` varchar(255) DEFAULT NULL COMMENT '主机',
  `ip` varchar(255) DEFAULT NULL COMMENT '被封禁IP',
  `create_time` timestamp NULL DEFAULT NULL COMMENT '添加时间',
  `operator` int(11) DEFAULT NULL COMMENT '操作人'
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COMMENT='IP封禁表';

--
-- 转存表中的数据 `ip_disabled`
--

INSERT INTO `ip_disabled` (`id`, `host_ip`, `ip`, `create_time`, `operator`) VALUES
(23, '121.43.138.234', '99.99.99.99', '2024-08-10 15:33:04', 1),
(29, '121.43.138.234', '172.16.136.122', '2024-08-10 19:23:34', 1);

-- --------------------------------------------------------

--
-- 表的结构 `menu_list`
--

CREATE TABLE `menu_list` (
  `id` int(11) NOT NULL,
  `parent_id` int(11) DEFAULT NULL,
  `name` varchar(100) NOT NULL,
  `icon` varchar(100) DEFAULT NULL,
  `url` varchar(255) DEFAULT NULL,
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- 转存表中的数据 `menu_list`
--

INSERT INTO `menu_list` (`id`, `parent_id`, `name`, `icon`, `url`, `create_time`) VALUES
(1, NULL, '系统管理', 'el-icon-s-home', NULL, '2024-08-04 09:48:48'),
(2, 1, '首页', 'el-icon-s-home', '/home', '2024-08-04 09:48:48'),
(3, NULL, '用户管理', 'el-icon-user-solid', NULL, '2024-08-04 09:48:48'),
(4, 3, '添加用户', 'el-icon-circle-plus', '/add', '2024-08-04 09:48:48'),
(5, 3, '用户列表', 'el-icon-circle-plus', '/user/list', '2024-08-04 09:48:48'),
(6, 3, '登录记录', 'el-icon-circle-plus', '/user/logpage', '2024-08-04 09:48:48'),
(7, NULL, '访问控制', 'el-icon-lock', NULL, '2024-08-04 09:48:48'),
(8, 7, '访问记录', 'el-icon-coin', '/packet/log', '2024-08-04 09:48:48'),
(9, 7, '封禁列表', 'el-icon-circle-plus', '/disabled_ip', '2024-08-04 09:48:48'),
(10, NULL, '网络监控', 'el-icon-view', NULL, '2024-08-04 09:48:48'),
(11, 10, '监测大屏', 'el-icon-c-scale-to-original', '/network/monitor', '2024-08-04 09:48:48'),
(12, NULL, '主机管理', 'el-icon-folder', '', '2024-08-04 17:21:22'),
(13, 12, '添加主机', 'el-icon-circle-plus-outline', '/host/add', '2024-08-04 17:21:53'),
(14, 12, '主机列表', 'el-icon-tickets', '/host/list', '2024-08-04 17:21:55'),
(15, 12, '主机概览', 'el-icon-tickets', '/host/info', '2024-08-04 17:21:55'),
(16, 10, '告警记录', 'el-icon-warning-outline', '/network/alert', '2024-08-04 17:21:55'),
(17, 12, '进程监控', 'el-icon-s-grid\n', '/host/processes', '2024-08-04 17:21:55'),
(18, NULL, '文件监控', 'el-icon-document', '', '2024-08-04 17:21:22'),
(19, 18, '改动记录', 'el-icon-document-remove', '/file/log', '2024-08-04 17:21:53');

-- --------------------------------------------------------

--
-- 表的结构 `packet_log`
--

CREATE TABLE `packet_log` (
  `id` int(11) NOT NULL,
  `host_ip` varchar(255) DEFAULT NULL COMMENT '主机IP',
  `src_ip` varchar(255) DEFAULT NULL COMMENT '源IP地址',
  `src_port` varchar(255) DEFAULT NULL COMMENT '源端口',
  `dst_ip` varchar(255) DEFAULT NULL COMMENT '目标IP',
  `dst_posrt` varchar(255) DEFAULT NULL COMMENT '目标端口',
  `potocol` varchar(100) DEFAULT NULL COMMENT '协议',
  `pack_size` double DEFAULT NULL COMMENT '包大小',
  `content` longtext COMMENT '包内容',
  `is_dangerous` int(10) DEFAULT NULL COMMENT '是否存在风险',
  `match` text COMMENT '报警命中',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='抓包记录';

-- --------------------------------------------------------

--
-- 表的结构 `permission_group`
--

CREATE TABLE `permission_group` (
  `id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `menu_nodes` json NOT NULL,
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- 转存表中的数据 `permission_group`
--

INSERT INTO `permission_group` (`id`, `name`, `menu_nodes`, `create_time`) VALUES
(1, '管理员', '[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]', '2024-08-04 09:49:08'),
(2, '用户', '[1, 2, 7, 8, 9, 10, 11, 12, 13, 15, 16, 17, 18, 19]', '2024-08-04 09:49:08');

-- --------------------------------------------------------

--
-- 表的结构 `system_load_data`
--

CREATE TABLE `system_load_data` (
  `id` int(11) NOT NULL,
  `ip` varchar(255) DEFAULT NULL COMMENT '来源IP',
  `data` text COMMENT 'JSON格式的数据',
  `create_time` datetime DEFAULT NULL COMMENT '创建时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='系统负载数据表';

-- --------------------------------------------------------

--
-- 表的结构 `traffic_data`
--

CREATE TABLE `traffic_data` (
  `id` int(11) NOT NULL,
  `ip` text NOT NULL,
  `total_sent` double NOT NULL,
  `total_received` double NOT NULL,
  `protocol_sizes` text NOT NULL,
  `timestamp` datetime DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

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
(47, 'aaa777', 0, '$2b$12$r/.buCi7wZekOyrx01rkg.IKfQxuWcBgO5Bq1u0gfxM8KLnnlyxJC', 'user', NULL, '2024-06-07 10:39:24'),
(48, 'test666', NULL, '$2b$12$nNZmmd4iICneeYqUec1B5uH7R9G1wzLAfw2e4LEmwVyqbiojUqZca', 'user', NULL, '2024-08-10 23:43:52');

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
(17, 1, '39.144.38.29', 'admin', '2024-06-08 09:16:23'),
(18, 1, '112.28.229.149', 'admin', '2024-06-08 12:49:07'),
(19, 1, '111.38.234.232', 'admin', '2024-06-09 09:53:45'),
(20, 1, '182.239.70.28', 'admin', '2024-06-12 04:54:33'),
(21, 1, '117.136.118.133', 'admin', '2024-06-13 08:42:21'),
(22, 1, '127.0.0.1', 'admin', '2024-08-02 13:30:28'),
(23, 1, '112.28.208.5', 'admin', '2024-08-04 12:23:47'),
(24, 1, '112.28.208.6', 'admin', '2024-08-08 06:30:14'),
(25, 1, '112.30.158.140', 'admin', '2024-08-10 15:47:30'),
(26, 48, '112.30.158.140', 'test666', '2024-08-10 15:48:39'),
(27, 1, '112.30.158.140', 'admin', '2024-08-11 02:14:37'),
(28, 1, '112.30.158.140', 'admin', '2024-08-11 02:38:31'),
(29, 1, '112.28.229.152', 'admin', '2024-08-11 03:16:52'),
(30, 1, '39.144.240.61', 'admin', '2024-08-11 20:32:06'),
(31, 1, '223.112.54.196', 'admin', '2024-08-11 20:58:36');

--
-- 转储表的索引
--

--
-- 表的索引 `alert_log`
--
ALTER TABLE `alert_log`
  ADD PRIMARY KEY (`id`);

--
-- 表的索引 `events`
--
ALTER TABLE `events`
  ADD PRIMARY KEY (`event_id`),
  ADD KEY `ix_events_event_id` (`event_id`);

--
-- 表的索引 `file_log`
--
ALTER TABLE `file_log`
  ADD PRIMARY KEY (`id`);

--
-- 表的索引 `hack_ip`
--
ALTER TABLE `hack_ip`
  ADD PRIMARY KEY (`hack_id`),
  ADD KEY `ix_hack_ip_hack_id` (`hack_id`);

--
-- 表的索引 `host_list`
--
ALTER TABLE `host_list`
  ADD PRIMARY KEY (`host_id`);

--
-- 表的索引 `ip_disabled`
--
ALTER TABLE `ip_disabled`
  ADD PRIMARY KEY (`id`);

--
-- 表的索引 `menu_list`
--
ALTER TABLE `menu_list`
  ADD PRIMARY KEY (`id`);

--
-- 表的索引 `packet_log`
--
ALTER TABLE `packet_log`
  ADD PRIMARY KEY (`id`);

--
-- 表的索引 `permission_group`
--
ALTER TABLE `permission_group`
  ADD PRIMARY KEY (`id`);

--
-- 表的索引 `system_load_data`
--
ALTER TABLE `system_load_data`
  ADD PRIMARY KEY (`id`);

--
-- 表的索引 `traffic_data`
--
ALTER TABLE `traffic_data`
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
-- 使用表AUTO_INCREMENT `alert_log`
--
ALTER TABLE `alert_log`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- 使用表AUTO_INCREMENT `events`
--
ALTER TABLE `events`
  MODIFY `event_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- 使用表AUTO_INCREMENT `file_log`
--
ALTER TABLE `file_log`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- 使用表AUTO_INCREMENT `hack_ip`
--
ALTER TABLE `hack_ip`
  MODIFY `hack_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- 使用表AUTO_INCREMENT `host_list`
--
ALTER TABLE `host_list`
  MODIFY `host_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- 使用表AUTO_INCREMENT `ip_disabled`
--
ALTER TABLE `ip_disabled`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=31;

--
-- 使用表AUTO_INCREMENT `menu_list`
--
ALTER TABLE `menu_list`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;

--
-- 使用表AUTO_INCREMENT `packet_log`
--
ALTER TABLE `packet_log`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- 使用表AUTO_INCREMENT `permission_group`
--
ALTER TABLE `permission_group`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- 使用表AUTO_INCREMENT `system_load_data`
--
ALTER TABLE `system_load_data`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- 使用表AUTO_INCREMENT `traffic_data`
--
ALTER TABLE `traffic_data`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- 使用表AUTO_INCREMENT `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=49;

--
-- 使用表AUTO_INCREMENT `user_log`
--
ALTER TABLE `user_log`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=32;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
