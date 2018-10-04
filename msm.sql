-- phpMyAdmin SQL Dump
-- version 4.8.3
-- https://www.phpmyadmin.net/
--
-- Anamakine: 127.0.0.1
-- Üretim Zamanı: 04 Eki 2018, 17:01:14
-- Sunucu sürümü: 10.1.36-MariaDB
-- PHP Sürümü: 7.2.10

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Veritabanı: `msm`
--

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `datam`
--

CREATE TABLE `datam` (
  `id` int(11) NOT NULL,
  `name` text NOT NULL,
  `email` varchar(50) NOT NULL,
  `password` text NOT NULL,
  `username` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=ucs2;

--
-- Tablo döküm verisi `datam`
--

INSERT INTO `datam` (`id`, `name`, `email`, `password`, `username`) VALUES
(1, 'selami uzun', 'selamiuzun2003@hotmail.com', 'selo', 'selamiuzun'),
(2, 'mert balcı', 'mert-balci@windowslive.com', 'mert12', 'mertbalci'),
(3, 'Fatih YILMAZ', 'memoylmz2@gmail.com', '26cishere', '26c'),
(4, 'Beyza günal', 'beyzagunal@gmail.com', 'beyza123', 'byzgünal'),
(5, 'revan uzun', 'revankaptan@gmail.com', 'maya', 'revanuzun'),
(6, 'Ece alara', 'ecealra07@gmail.com', 'ece123.', 'ecealara'),
(7, 'Erva Mut', 'ervoaa@gmail.com', 'malaklar07', 'ervamut'),
(8, 'göksu', 'goksuvural@gmail.com', 'bafra2002', 'göksuvural'),
(9, 'selami uzun', 'selamiuzun2003@hotmail.com', '1234', 'memoylmz'),
(12, 'Mdjsks', 'Jdjsjsjs@hdjskka.com', 'asd', 'Asdshhs'),
(13, 'ece alara', 'ecealra07@gmail.com', 'ece123', 'ece alara');

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `makale`
--

CREATE TABLE `makale` (
  `id` int(11) NOT NULL,
  `author` text NOT NULL,
  `title` text NOT NULL,
  `content` text NOT NULL,
  `date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Tablo döküm verisi `makale`
--

INSERT INTO `makale` (`id`, `author`, `title`, `content`, `date`) VALUES
(1, 'selamiuzun', 'Bakıt açılış', '<p>Anasayfada da belirttiğimiz &uuml;zere T&uuml;rkiye&#39;de teknolojik a&ccedil;ıdan gelişimi hızlandırmak i&ccedil;in b&ouml;yle bir oluşuma ihtiya&ccedil; duyulduğunu &ouml;ng&ouml;rd&uuml;k. Sitenin bu b&ouml;l&uuml;m&uuml;nde ise bilirkişilerden &ccedil;eşitli makalelere yer verilecektir.</p>\r\n', '2018-10-04 14:56:33');

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `soru`
--

CREATE TABLE `soru` (
  `id` int(11) NOT NULL,
  `title` text NOT NULL,
  `content` text NOT NULL,
  `author` text NOT NULL,
  `date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `yanıt` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=ucs2;

-- --------------------------------------------------------

--
-- Tablo için tablo yapısı `yanıt`
--

CREATE TABLE `yanıt` (
  `id` int(11) NOT NULL,
  `author` text NOT NULL,
  `yanıt` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dökümü yapılmış tablolar için indeksler
--

--
-- Tablo için indeksler `datam`
--
ALTER TABLE `datam`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`,`username`);

--
-- Tablo için indeksler `makale`
--
ALTER TABLE `makale`
  ADD PRIMARY KEY (`id`);

--
-- Tablo için indeksler `soru`
--
ALTER TABLE `soru`
  ADD PRIMARY KEY (`id`);

--
-- Dökümü yapılmış tablolar için AUTO_INCREMENT değeri
--

--
-- Tablo için AUTO_INCREMENT değeri `datam`
--
ALTER TABLE `datam`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- Tablo için AUTO_INCREMENT değeri `makale`
--
ALTER TABLE `makale`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- Tablo için AUTO_INCREMENT değeri `soru`
--
ALTER TABLE `soru`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
