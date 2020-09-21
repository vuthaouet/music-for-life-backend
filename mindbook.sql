-- MySQL dump 10.13  Distrib 5.7.29, for Linux (x86_64)
--
-- Host: 127.0.0.1    Database: mindbook
-- ------------------------------------------------------
-- Server version	5.7.29

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `author_details`
--

DROP TABLE IF EXISTS `author_details`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `author_details` (
  `author_id` int(11) NOT NULL AUTO_INCREMENT,
  `author_name` varchar(120) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  PRIMARY KEY (`author_id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `author_details`
--

LOCK TABLES `author_details` WRITE;
/*!40000 ALTER TABLE `author_details` DISABLE KEYS */;
INSERT INTO `author_details` VALUES (1,'Nhiều tác giả'),(2,'James Allen'),(3,'Phạm Quốc Hưng'),(4,'Chin Ning Chu'),(5,'Lão Mạc'),(6,'Vladimir Soloviev'),(7,'Tony Buổi Sáng'),(8,'Nguyễn Thị Hà Bắc'),(9,'Nguyễn đổng Chi');
/*!40000 ALTER TABLE `author_details` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `book_categories`
--

DROP TABLE IF EXISTS `book_categories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `book_categories` (
  `book_id` int(11) NOT NULL,
  `category_id` int(11) NOT NULL,
  PRIMARY KEY (`book_id`,`category_id`),
  KEY `category_id` (`category_id`),
  CONSTRAINT `book_categories_ibfk_1` FOREIGN KEY (`book_id`) REFERENCES `book_details` (`book_id`),
  CONSTRAINT `book_categories_ibfk_2` FOREIGN KEY (`category_id`) REFERENCES `category_details` (`category_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `book_categories`
--

LOCK TABLES `book_categories` WRITE;
/*!40000 ALTER TABLE `book_categories` DISABLE KEYS */;
INSERT INTO `book_categories` VALUES (9,1),(4,2),(8,3),(3,4),(2,5),(9,6),(7,7),(1,8),(5,8),(6,8),(4,9),(2,10),(3,11),(10,12),(1,13),(5,13),(6,13),(8,14);
/*!40000 ALTER TABLE `book_categories` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `book_details`
--

DROP TABLE IF EXISTS `book_details`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `book_details` (
  `book_id` int(11) NOT NULL AUTO_INCREMENT,
  `book_title_vi` varchar(200) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `book_title_en` varchar(200) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `book_description_vi` text CHARACTER SET utf8 COLLATE utf8_bin,
  `book_description_en` text CHARACTER SET utf8 COLLATE utf8_bin,
  `author_id` int(11) DEFAULT NULL,
  `book_cover` varchar(200) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  `book_epub` varchar(200) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  PRIMARY KEY (`book_id`),
  KEY `author_id` (`author_id`),
  CONSTRAINT `book_details_ibfk_1` FOREIGN KEY (`author_id`) REFERENCES `author_details` (`author_id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `book_details`
--

LOCK TABLES `book_details` WRITE;
/*!40000 ALTER TABLE `book_details` DISABLE KEYS */;
INSERT INTO `book_details` VALUES (1,'Khi Người Ta Tư Duy',NULL,'Hơn một thế kỷ đã trôi qua kể từ lần xuất bản đầu tiên vào năm 1902, “Khi người ta tư duy” vẫn luôn là một trong những kiệt tác bán chạy nhất và liên tiếp nhận được sự tán dương, ca ngợi từ độc giả. Với hàng triệu bản được ấn hành, cuốn sách đã truyền cảm hứng tới hàng triệu người trên toàn thế giới. \n Nội dung xuyên suốt của cuốn sách rất đơn giản: con người bạn ở hiện tại và tương lai chính là những gì bạn tư duy và mơ ước. Tuy không có dung lượng đồ sộ nhưng với cách viết súc tích và thuyết phục, cuốn sách xinh xắn này chắc chắn không phải chỉ để đọc một lần, mà sẽ là hành trang quý giúp bạn khám phá sức mạnh lớn lao của bộ óc con người và làm chủ sức mạnh kỳ diệu ấy. \n James Allen (1864 – 1912) là triết gia nổi tiếng người Anh,từng rời bỏ công việc kinh doanh để sống cuộc đời gắn liền với viết lách và suy ngẫm. Ông là tác giả của những cuốn sách kinh điển trong thể loại duy linh và truyền cảm hứng. Nổi tiếng nhất với cuốn “As a man thinketh”, James Allen còn là tác giả của một số cuốn sách khác nói về sức mạnh của tư duy như: Đường tới phồn vinh (The Path to Prosperity), Làm chủ số phận (The Mastery of Distiny), Phương pháp hòa bình (The Way of Peace)…',NULL,2,'https://i.imgur.com/Nk1IAAf.jpg','khi-nguoi-ta-tu-duy-james-allen.epub'),(2,'Kinh Nghiệm Thành Công Của Ông Chủ Nhỏ',NULL,'Kinh Nghiệm Thành Công Của Ông Chủ Nhỏ là một cuốn sách có nội dung khác biệt với những cuốn sách kinh doanh thông thường khác, có thể sẽ giúp ích được cho những bạn trẻ đã và đang dấn thân vào lĩnh vực kinh doanh. Trong cuốn sách này, trước tiên, tác giả nêu ra tình huống, sau đó đi sâu phân tích, đưa ra những luận điểm về những tình tiết quan trọng trong câu chuyện và đề cập tới những lĩnh vực có thể ứng dụng luận điểm đó. Những câu chuyện mà tác giả viết ra không được phân loại theo phương thức quản lí kinh doanh mà dựa theo đặc điểm cách làm của doanh nghiệp. Và đặc biệt, đó không phải là những câu chuyện quen thuộc từng được đề cập trong giáo trình thương mại, mà phần lớn là những điều tâm đắc và những trải nghiệm của chính tác giả. \nCuốn sách này không đơn thuần là chuyện bán bánh nướng, bán chân giò xông khói... thế nào cho đắt hàng như nhiều người thoạt tưởng. Thực ra nó là chuyện lên kế hoạch và thực hiện chiến lược để có thể khống chế được cục diện, vừa phát triển nghể, vừa hạn chế được đối thủ cạnh tranh của một ông chủ.Vì vậy, cuốn sách không chỉ có ích cho những người làm kinh doanh nhỏ, mà còn hữu ích với cả những ông chủ lớn.',NULL,5,'https://i.imgur.com/NOiapEt.jpg','kinh-nghiem-thanh-cong-cua-ong-chu-nho-lao-mac.epub'),(3,'Pr Là Sống',NULL,'PR là một chức năng quản trị định hướng thái độ của công chúng, xác định chính sách, thực hiện và làm cho quan tâm một tổ chức, được thực hiện theo một chương trình hành động tìm kiếm sự thông hiểu và chấp nhận của công chúng” theo lời một nữ chuyên gia PR định nghĩa. \nNgày nay trong bất cứ ngành nào, PR vẫn rất quan trọng. PR thể hiện tầm quan trọng trong giao tiếp của một tổ chức hay một cá nhân và đối tượng của họ như là nhân viên, đối tác, nhóm cần quan tâm. Đặc biệt, chúng ta có thể thấy sức mạnh của PR trong lĩnh vực dịch vụ như ngân hàng, tài chính, vận tải, du lịch, nhà hàng, khách sạn mà các hoạt động của con người cần sự giao tiếp tốt để có hiệu quả công việc cao. \nBằng tất cả nỗ lực, tác giả đã cố gắng thực hiện và hoàn thành cuốn sách này. Hy vọng tất cả trải nghiệm, suy nghĩ, ý tưởng và cảm nhận của tác giả có thể đóng góp một phần vào sự hoàn hảo của cộng đồng PR. PR không tự nó là phương thuốc diệu kỳ cho sự vững mạnh của thương hiệu mà ở tại người nhìn nhận và sử dụng nó như thế nào. Với các nguyên tắc 3PR, 3S, CAR, NCNS, và ANGEL STARS, PR sẽ thật sự sống mãi cùng thương hiệu của từng tổ chức và cuộc đời của mỗi người.',NULL,3,'https://i.imgur.com/hKd6L5c.jpg','pr-la-song-pham-quoc-hung.epub'),(4,'Bão Lửa U23 – Thường Châu Tuyết Trắng',NULL,'Như chúng ta đều biết, những thành quả mà Đội tuyển U23 Việt Nam đạt được tại VCK U23 châu Á 2018 đã mang lại những cảm xúc khó quên trong lòng mỗi người con đất Việt. Những cảm hứng tuyệt vời đó thật hiếm hoi và đáng quý, cần được lan tỏa, lưu giữ theo thời gian, để luôn  nhắc nhở chúng ta rằng, người Việt giàu tinh thần dân tộc, tinh thần thượng võ, giàu ý chí, nghị lực, đặc biệt là trước những thử thách, nghịch cảnh. Thế hệ trẻ Việt Nam hoàn toàn có thể chinh phục những đỉnh cao trong nhiều lĩnh vực khác như kinh tế, giáo dục, khoa học kỹ thuật… như trong thể thao như U23 đã làm được. \nXuất phát từ nguồn cảm hứng tuyệt vời mà sự kiện U23 mang lại và lan tỏa trên cả nước trong thời gian qua, chúng tôi  – Ban Dự án Bão Lửa của Sống – Thương hiệu sách Tác giả Việt của Alpha Books đã triển khai thực hiện cuốn sách Bão lửa U23 – Thường Châu tuyết trắng nhằm tri ân tập thể cán bộ, cầu thủ U23 Việt Nam – những anh hùng trên sân cỏ, HLV Park Hang Seo cùng các thành viên Ban huấn luyện, các ông bầu Đoàn Nguyên Đức, Đỗ Quang Hiển… những người đã tâm huyết gây dựng, tận lực cống hiến cho thắng lợi vang dội của bóng đá Việt Nam trong sự kiện vừa qua. \nCuốn sách tập hợp gần 50 bài viết chất lượng, cô đọng và sâu sắc của nhiều cây bút thể thao có tiếng như Trương Anh Ngọc, Phạm Trung Tuyến, Hoàng Linh, Nguyên Khôi, Quốc Việt…; của các tác giả, nhà văn, nhà nghiên cứu thuộc nhiều lĩnh vực khác nhau, như Chu Văn Sơn, Nguyễn Quang Thiều, Đinh Hoàng Anh, Trần Vinh Dự, Nguyễn Cảnh Bình,... đặc biệt là có sự tham gia của Lê Huy Khoa – Trợ lý ngôn ngữ HLV Park Hang Seo. \nĐã có rất nhiều những bài báo viết về chiến công của đội tuyển U23 trong quãng thời gian ngắn ngủi vừa qua. Nhưng cuốn sách này khác hẳn với những gì đã được viết ra, đơn giản vì nó không chỉ cô đọng lại từng khoảnh khắc của những trận đấu đã qua, những hiệu ứng cảm xúc kỳ diệu U23 đã mang lại cho cả dân tộc, mà còn cung cấp những cái nhìn rất sâu về từng khía cạnh của những nguyên nhân và chân dung những con người đã làm nên chiến thắng, những khó khăn đã trải qua, những rắc rối gặp phải trên đường vào chung kết, nhưng cũng không quên nhắc đến con đường tiếp theo của bóng đá Việt Nam sau thành công này. \nĐặc biệt hơn, cuốn sách cung cấp những bài viết bàn về kinh nghiệm sâu sắc rút ra sau sự kiện U23 không chỉ cho chính lĩnh vực thể thao mà cho nhiều lĩnh vực khác như giáo dục – đào tạo, quản lý, kinh tế… \nXu hướng là thứ nhất thời nhưng cảm xúc chân thật sẽ còn đọng lại mãi. Cuốn sách Bão lửa U23 – Thường Châu tuyết trắng lưu giữ những cảm xúc chân thật của người hâm mộ bóng đá Việt Nam, của chính các tuyển thủ và những người làm chuyên môn… qua từng chặng đường, từng khoảnh khắc hiếm có. Cuốn sách sẽ đóng vai một chứng nhân lịch sử, một người đã đi qua giây phút bi tráng và hào hùng của dân tộc để ghi lại những thước phim tư liệu quý. Nó ra đời và tồn tại vì ngay khoảnh khắc đó những con tim Việt Nam đã xích lại gần nhau thân thương, ấm áp và rạng rỡ, ngay khoảnh khắc đó chúng ta yêu U23, tình yêu mãnh liệt và chân thành nhất! \nĐây là một cuốn sách rất đáng đọc vào lúc này, khi những dư âm của chiến công U23 vẫn còn, nhưng cũng là để ngẫm ngợi sâu hơn về nhiều điều liên quan đến họ nói riêng và cả nền bóng đá Việt Nam nói chung.',NULL,1,'https://i.imgur.com/CHfv9wM.jpg','bao-lua-u23-–-thuong-chau-tuyet-trang-nhieu-tac-gia.epub'),(5,'Làm Ít Được Nhiều',NULL,'Trong thời đại thay đổi nhanh chóng và cạnh tranh gay gắt hiện nay, chúng ta thường tự vướng vào một quan điểm quá mệt mỏi là tin rằng thành công chỉ đến khi phải đánh đổi bằng sự cân bằng của cuộc sống. Tuy nhiên, hầu hết những người thành công lại không nhất thiết phải làm việc vất vả. Trong quyển Làm ít được nhiều, tác giả có sách bán chạy Ching-Nin-Chu giải thích cách làm thế nào để giải tỏa cái vòng lẩn quẩn đó và học cách để vừa bình an vừa hiệu quả cùng một lúc. \nHọc cách làm thế nào để: \n	• Sử dụng Bộ ba bí mật để giải phóng năng lực của bản thân; \n	• Đặt mình vào tâm điểm của công việc, hành động một cách tập trung, đồng thời cân bằng cuộc sống; \n	• Đạt được mục tiêu mà chỉ cần làm việc và lo lắng ít thôi; \n	• Có thời gian và sự thảnh thơi để hưởng thụ thành quả lao động. \n“Chúng ta không đạt được mục tiêu vì chúng ta nỗ lực quá nhiều để tìm kiếm thành công. Bí mật - như Ching-Nin-Chu cho biết - là tìm ra điểm cân bằng giữa nỗ lực và sự thoải mái.”',NULL,4,'https://i.imgur.com/Drqwtle.jpg','lam-it-duoc-nhieu-chin-ning-chu.epub'),(6,'Tony Buổi Sáng - Trên Đường Băng',NULL,'Trên đường băng là tập hợp những bài viết được ưa thích trên Facebook của Tony Buổi Sáng. Nhưng khác với một tập tản văn thông thường, nội dung các bài được chọn lọc có chủ đích, nhằm chuẩn bị về tinh thần, kiến thức…cho các bạn trẻ vào đời. Sách gồm 3 phần: “Chuẩn bị hành trang”, “Trong phòng chờ sân bay” và “Lên máy bay”, tương ứng với những quá trình một bạn trẻ phải trải qua trước khi “cất cánh” trên đường băng cuộc đời, bay vào bầu trời cao rộng. \nNhững bài viết của Tony sinh động, thiết thực, hài hước và xuất phát từ cái tâm trong sáng của một người đi trước nhiều kinh nghiệm. Anh viết về thái độ với sự học và kiến thức nói chung, cách ứng phó với những trắc trở thử thách khi đi làm, cách sống hào sảng nghĩa tình văn minh…truyền cảm hứng cho các bạn trẻ sống hết mình, trọn vẹn từng phút giây. Tuy đối tượng độc giả chính mà cuốn sách hướng đến là các bạn trẻ, nhưng độc giả lớn tuổi hơn vẫn có thể đọc sách để hiểu và có cách hỗ trợ con em mình một cách đúng đắn, chứ không “ủ” con quá kỹ để rồi tạo ra một thế hệ yếu ớt, không biết tự lập. Những người đi làm nhiều năm đọc sách cũng có thể nhìn lại con đường đi của mình, tự ngẫm đó đã phải là con đường mình muốn đi chưa, bởi thay đổi không bao giờ là quá muộn.',NULL,7,'https://i.imgur.com/lV8atgV.jpg','tony-buoi-sang-tren-duong-bang-tony-buoi-sang.epub'),(7,'Tự Học Tiếng Anh Hiệu Quả',NULL,'Nếu  như bạn  mong  muốn  giao  tiếp  tiếng  Anh  thành  thạo,  chuyên nghiệp từ 3 tới 6 tháng thì cuốn sách này sẽ làm bạn thất vọng. Thực tế cho thấy chưa có ai mới bắt đầu học tiếng  Anh có thể giao tiếp được trôi chảy trong thời gian từ 3 – 6 tháng. Đó là ảo tưởng. Nhưng nếu như bạn đang tìm kiếm làm như thế nào có thể sử dụng tiếng Anh giao tiếp thành thạo, chuyên nghiệp trong 1 năm tới thì xin chúc mừng  bạn.  Tôi tin rằng  những  bí  mật  được tiết  lộ  trong  cuốn sách này sẽ làm bạn thỏa mãn với điều đó. \nCó rất nhiều người học tiếng Anh lâu năm nhưng vẫn không giao tiếp được. Có những người học tiếng Anh tại các trung tâm khác nhau nhưng vẫn không giao tiếp được. Hầu hết chúng ta học ngoại ngữ gần 12 năm cũng không giao tiếp được. Phải chăng có điều gì đó mà những người chúng ta còn thiếu? \nCuốn sách này sẽ chỉ ra cho bạn thấy yếu tố then chốt để thành công với  tiếng Anh. Nó không phải là phương pháp học, nó cũng không phải là môi trường, cũng không phải là đối tác .. \nTuy nhiên trong bất kỳ cuộc thi hay cuộc chơi nào cũng vậy cả, thường chỉ có 5% là những người xuất sắc vượt trội và đạt được những thành tích đáng ngưỡng mộ. Chính vì vậy bạn có quyền lựa chọn, ở khu vực 95% hay 5% là do bạn quyết định. Rất nhiều người đọc cuốn sách này. Nhưng 95% mọi người không đọc hết nó và đó chính là cách mà những người đó đã thất bại. Bởi vì cách mà họ bỏ cuộc trong một cuộc thi nhỏ là đọc hết một cuốn sách này thì đó cũng chính là cách họ bỏ cuộc trong hành trình học tiếng anh.  Nhưng tôi tin, bạn sẽ lựa chọn đứng vào top 5% những người xuất sắc nhất, phải không nào? \nNếu như bạn đã sẵn sàng để sử dụng tiếng Anh trong 1 năm tới thì tôi  tin  chắc rằng  đây  chính  là  quyển  sách  quan trọng  nhất  mà  bạn cần  đọc.  Hãy  đọc,  tin tưởng  và  thực  hành.  Tôi tin  rằng  bạn  sẽ  đạt được kết quả kỳ diệu trong 1 năm tới.',NULL,8,'https://i.imgur.com/UeR0Ils.jpg','tu-hoc-tieng-anh-hieu-qua-nguyen-thi-ha-bac.epub'),(8,'Kho Tàng Truyện Cổ Tích Việt Nam',NULL,'KHO TÀNG TRUYỆN CỔ TÍCH VIỆT NAM,kể từ lần in thứ bảy, in cùng lúc trọn bộ cả năm tập. Rất tiếc, ở những lần in toàn vẹn này tác giả đã không còn được tự mình xem lại bản in thử, như ông đã từng làm việc đó một cách hứng thú và kiên trì trong sáu lần in lẻ tẻ từng tập trước đây. \nTuy nhiên, từ sau khi tập V ra mắt (1982), thân phụ chúng tôi đã có dịp chỉnh lý kỹ cả năm tập, nhất là phần Tổng luận, nhằm chuẩn bị cho một lần in đầy đủ sau này. Chúng tôi cố gắng trung thành với những sửa chữa trực tiếp của ông, kể cả một đôi chỗ ông ủy thác cho tôi soát lại chút ít ít câu chữ, trong khi đọc bộ sách. Mặt khác, trong lần in thứ tư (1972), tác giả có một thay đổi đáng kể trong kết cấu cuốn sách của mình: ông bỏ đi 2 truyện và thay bằng 2 truyện khác để giữ nguyên số lượng 200 truyện. \nCân nhắc kỹ lại trong lần in thứ bảy, chúng tôi đã mạnh dạn đưa một truyện trong số đó trở lại bộ sách: truyện Giết chó khuyên chồng, số 50. Để bạn đọc dễ nhận ra truyện này đã được bỏ đi, chúng tôi đặt chữ số 50 đứng đầu tên truyện trong dấu [ ]. Tôn trọng ý nguyện của tác giả, các quy tắc viết hoa và phiên âm tên người, tên đất vẫn giữ nguyên như trong mấy lần in trước chứ không thay đổi. Tuy vậy, để giúp các nhà nghiên cứu có thể tra tìm nhanh chóng khối lượng tài liệu nước ngoài hết sức lớn mà tác giả đã tham khảo, ở các chú thích xuất xứ, bên cạnh tên người phiên âm trước đây chúng tôi có ký chú thêm nguyên văn, hoặc chuyển ngữ tiếng Pháp. Đối với tên một số dân tộc, hay một số địa danh trên thế giới được nhắc đến trong mục Khảo dị, nếu thấy cần thiết, chúng tôi cũng làm như vậy. Cuối bộ sách, chúng tôi còn thêm vào một Bảng tra cứu tên truyện sắp xếp theo trật tự a b c. Tất cả những việc này đều do các bạn bè thân thiết trong Ban văn học Cổ cận đại Viện Văn học góp sức thực hiện vào năm 1992.',NULL,9,'https://i.imgur.com/yUhZhUj.jpg','Kho-Tang-Truyen-Co-Tich.epub'),(9,'Dữ Liệu Lớn - Big Data',NULL,'Màu sơn nào có thể cho bạn biết một chiếc xe đã qua sử dụng vẫn còn trong tình trạng tốt? Làm thế nào các công chức ở thành phố New York có thể xác định các hố ga nguy hiểm nhất trước khi chúng phát nổ? Và làm thế nào những cuộc tìm kiếm của Google dự đoán được sự lây lan của dịch cúm H1N1? \nChìa khóa để trả lời những câu hỏi này, và nhiều câu hỏi khác, là dữ liệu lớn. \'Dữ liệu lớn\' đề cập đến khả năng đang phát triển của chúng ta để nắm giữ các bộ sưu tập lớn thông tin, phân tích, và rút ra những kết luận đôi khi sâu sắc đáng ngạc nhiên. Lĩnh vực khoa học đang nổi lên này có thể chuyển vô số hiện tượng – từ giá vé máy bay đến các văn bản của hàng triệu cuốn sách – thành dạng có thể tìm kiếm được, và sử dụng sức mạnh tính toán ngày càng tăng của chúng ta để khám phá những điều chúng ta chưa bao giờ có thể nhìn thấy trước. Trong một cuộc cách mạng ngang tầm với Internet hoặc thậm chí in ấn, dữ liệu lớn sẽ thay đổi cách chúng ta nghĩ về kinh doanh, y tế, chính trị, giáo dục, và sự đổi mới trong những năm tới. Nó cũng đặt ra những mối đe dọa mới, từ sự kết thúc không thể tránh khỏi của sự riêng tư cho đến khả năng bị trừng phạt vì những thứ chúng ta thậm chí còn chưa làm, dựa trên khả năng của dữ liệu lớn có thể dự đoán được hành vi tương lai của chúng ta. \nTrong tác phẩm thông tuệ tuyệt vời và gây nhiều ngạc nhiên này, hai chuyên gia hàng đầu giải thích dữ liệu lớn là những gì, nó sẽ làm thay đổi cuộc sống của chúng ta như thế nào, và những gì chúng ta có thể làm để bảo vệ chính mình khỏi các mối nguy hiểm của nó. Dữ liệu lớn là cuốn sách lớn đầu tiên về điều to lớn sắp diễn ra.”',NULL,1,'https://i.imgur.com/1cGi7Io.jpg','du-lieu-lon-big-data.epub'),(10,'Siêu Lý Tình Yêu',NULL,'Soloviev chỉ ra 5 loại quan hệ nam nữ với loại quan hệ nam nữ có tình yêu gắn với lý tưởng hóa đối tượng yêu, làm chúng ta khi yêu mang bản nguyên thần thánh. Tình yêu nam - nữ tuyệt đích sẽ bất tử hóa tất cả bởi tình yêu chuyên trở sự sống vĩnh cửu cho cái mình yêu, tái sinh vĩnh viễn trong cái đẹp. \nĐó là luận điểm về tình yêu qua các tác phẩm trứ danh: Siêu lý tình yêu (1892-1893), Chiến tranh và hòa bình, Biện minh cái thiện của Vladimir Solovyev, người nhà văn, đại triết gia Nga - người đặt nền móng cho Triết học Tình yêu châu Âu.',NULL,6,'https://i.imgur.com/pRaHZo0.jpg','sieu-ly-tinh-yeu-vladimir-soloviev.epub');
/*!40000 ALTER TABLE `book_details` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `category_details`
--

DROP TABLE IF EXISTS `category_details`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `category_details` (
  `category_id` int(11) NOT NULL AUTO_INCREMENT,
  `category_name` varchar(120) CHARACTER SET utf8 COLLATE utf8_bin DEFAULT NULL,
  PRIMARY KEY (`category_id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `category_details`
--

LOCK TABLES `category_details` WRITE;
/*!40000 ALTER TABLE `category_details` DISABLE KEYS */;
INSERT INTO `category_details` VALUES (1,'Kỹ Thuật'),(2,'Thể Thao'),(3,'Thần Thoại'),(4,'Marketing'),(5,'Kinh Tế'),(6,'Khoa Học'),(7,'Học Ngoại Ngữ'),(8,'Kỹ Năng Sống'),(9,'Nghệ Thuật'),(10,'Quản Lý'),(11,'Bán hàng'),(12,'Triết Học'),(13,'Tâm Lý'),(14,'Cổ Tích');
/*!40000 ALTER TABLE `category_details` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rating_details`
--

DROP TABLE IF EXISTS `rating_details`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `rating_details` (
  `user_id` int(11) NOT NULL,
  `book_id` int(11) NOT NULL,
  `rating_num` int(11) DEFAULT NULL,
  `rating_comment` text CHARACTER SET utf8 COLLATE utf8_bin,
  PRIMARY KEY (`user_id`,`book_id`),
  KEY `book_id` (`book_id`),
  CONSTRAINT `rating_details_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user_details` (`user_id`),
  CONSTRAINT `rating_details_ibfk_2` FOREIGN KEY (`book_id`) REFERENCES `book_details` (`book_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rating_details`
--

LOCK TABLES `rating_details` WRITE;
/*!40000 ALTER TABLE `rating_details` DISABLE KEYS */;
/*!40000 ALTER TABLE `rating_details` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `revoked_tokens`
--

DROP TABLE IF EXISTS `revoked_tokens`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `revoked_tokens` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `jti` varchar(120) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `revoked_tokens`
--

LOCK TABLES `revoked_tokens` WRITE;
/*!40000 ALTER TABLE `revoked_tokens` DISABLE KEYS */;
/*!40000 ALTER TABLE `revoked_tokens` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_details`
--

DROP TABLE IF EXISTS `user_details`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user_details` (
  `user_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_name` varchar(120) NOT NULL,
  `email` varchar(120) NOT NULL,
  `password` varchar(120) NOT NULL,
  `first_name` varchar(50) NOT NULL,
  `last_name` varchar(50) NOT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_details`
--

LOCK TABLES `user_details` WRITE;
/*!40000 ALTER TABLE `user_details` DISABLE KEYS */;
/*!40000 ALTER TABLE `user_details` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-04-20 13:11:09
