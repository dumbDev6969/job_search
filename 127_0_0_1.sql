-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jun 03, 2025 at 02:49 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `basics`
--
CREATE DATABASE IF NOT EXISTS `basics` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE `basics`;

-- --------------------------------------------------------

--
-- Table structure for table `cache`
--

CREATE TABLE `cache` (
  `key` varchar(255) NOT NULL,
  `value` mediumtext NOT NULL,
  `expiration` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `cache_locks`
--

CREATE TABLE `cache_locks` (
  `key` varchar(255) NOT NULL,
  `owner` varchar(255) NOT NULL,
  `expiration` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `migrations`
--

CREATE TABLE `migrations` (
  `id` int(10) UNSIGNED NOT NULL,
  `migration` varchar(255) NOT NULL,
  `batch` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `migrations`
--

INSERT INTO `migrations` (`id`, `migration`, `batch`) VALUES
(8, '0001_01_01_000000_create_users_table', 1),
(9, '0001_01_01_000001_create_cache_table', 1),
(10, '2025_02_13_071839_create_offices_table', 1),
(11, '2025_02_13_071910_create_workers_table', 1);

-- --------------------------------------------------------

--
-- Table structure for table `offices`
--

CREATE TABLE `offices` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL,
  `office_leader` varchar(255) NOT NULL,
  `office_number` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `offices`
--

INSERT INTO `offices` (`id`, `created_at`, `updated_at`, `office_leader`, `office_number`) VALUES
(1, '2025-02-13 00:47:38', '2025-02-13 00:47:38', 'Prof. Pierre Aufderhar Sr.', 6),
(2, '2025-02-13 00:47:38', '2025-02-13 00:47:38', 'Gerry Leuschke', 2),
(3, '2025-02-13 00:47:38', '2025-02-13 00:47:38', 'Mrs. Shania Rohan', 11),
(4, '2025-02-13 00:47:38', '2025-02-13 00:47:38', 'Myrtis Smitham', 3),
(5, '2025-02-13 00:47:38', '2025-02-13 00:47:38', 'Kieran Stanton', 4),
(6, '2025-02-13 00:47:38', '2025-02-13 00:47:38', 'Jaida McCullough II', 12),
(7, '2025-02-13 00:47:38', '2025-02-13 00:47:38', 'Mr. Delaney Borer IV', 1),
(8, '2025-02-13 00:47:38', '2025-02-13 00:47:38', 'Freida Schaden', 9),
(9, '2025-02-13 00:47:38', '2025-02-13 00:47:38', 'Louisa Friesen', 7),
(10, '2025-02-13 00:47:38', '2025-02-13 00:47:38', 'Dr. Loma Rippin MD', 8),
(11, '2025-02-13 00:47:38', '2025-02-13 00:47:38', 'Linnea Collier DDS', 10),
(12, '2025-02-13 00:47:38', '2025-02-13 00:47:38', 'Kristina Schowalter', 5);

-- --------------------------------------------------------

--
-- Table structure for table `password_reset_tokens`
--

CREATE TABLE `password_reset_tokens` (
  `email` varchar(255) NOT NULL,
  `token` varchar(255) NOT NULL,
  `created_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `sessions`
--

CREATE TABLE `sessions` (
  `id` varchar(255) NOT NULL,
  `user_id` bigint(20) UNSIGNED DEFAULT NULL,
  `ip_address` varchar(45) DEFAULT NULL,
  `user_agent` text DEFAULT NULL,
  `payload` longtext NOT NULL,
  `last_activity` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `sessions`
--

INSERT INTO `sessions` (`id`, `user_id`, `ip_address`, `user_agent`, `payload`, `last_activity`) VALUES
('42HEJDKC8JstNegv0MdmvT66mLs2GEgK5XeaxycB', NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36', 'YTozOntzOjY6Il90b2tlbiI7czo0MDoiOXlyRU9MWUVkSFJTcmJqN2dVZzZBQmVBOWs5SDVacFY5bm9XNTUzSCI7czo2OiJfZmxhc2giO2E6Mjp7czozOiJvbGQiO2E6MDp7fXM6MzoibmV3IjthOjA6e319czo5OiJfcHJldmlvdXMiO2E6MTp7czozOiJ1cmwiO3M6MjQ6Imh0dHA6Ly9iYXNpY3MudGVzdC9hZG1pbiI7fX0=', 1739849845);

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `name` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `email_verified_at` timestamp NULL DEFAULT NULL,
  `password` varchar(255) NOT NULL,
  `remember_token` varchar(100) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `workers`
--

CREATE TABLE `workers` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL,
  `name` varchar(255) NOT NULL,
  `age` int(11) NOT NULL,
  `bio` text NOT NULL,
  `office_id` bigint(20) UNSIGNED NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `workers`
--

INSERT INTO `workers` (`id`, `created_at`, `updated_at`, `name`, `age`, `bio`, `office_id`) VALUES
(4, '2025-02-13 00:47:38', '2025-02-13 00:47:38', 'Arthur McKenzie MD', 53, 'Id itaque nesciunt ipsa qui expedita dolor quas quisquam. Et accusantium tempora et officia. Blanditiis adipisci quia non quis. Facere quisquam dolorem iste similique. Omnis quod dolor inventore accusantium. Fugit voluptatum et quas eveniet et est. Et ad quasi debitis veritatis eum aut aut. Quidem nesciunt facere qui. Rerum tempora est adipisci iste illo tenetur quasi. Deserunt officia ut occaecati autem omnis voluptates. Nostrum architecto et exercitationem adipisci. Velit et ut aut aut eaque sed consequuntur est. Sed magnam unde consequatur fugiat. Rem et ipsam tenetur. Exercitationem animi sint possimus porro. Voluptatem ipsum et beatae praesentium officiis saepe qui. Eos omnis consequatur quibusdam facilis et quasi harum. Nihil voluptas molestiae qui quaerat est laboriosam tenetur. Ut sit occaecati dolor nisi sunt quis. Atque nihil consequatur blanditiis aut ut dicta sit. Sit quaerat unde dolor nulla distinctio enim qui. Dicta velit maxime odio voluptatem modi eos. Consectetur iure facilis temporibus deleniti harum repellendus rerum. Eaque aliquam aut molestias ea nulla. Repellendus facere veritatis laborum nulla autem optio. Non ut eius qui ipsam rerum sunt. Iste vel maiores ut expedita dolores. Magni placeat odit qui dicta aliquid dolorem. Ex accusamus saepe exercitationem assumenda ipsam quia tempore. Quas quisquam quo nam unde quod voluptatibus. Sunt ratione consectetur tenetur dolorum odit molestias. Nesciunt accusamus ratione aliquam a maiores et soluta. Ea autem consequatur praesentium facere pariatur in voluptatum. Facere tempore in minima odit aut possimus. Qui illum quia rerum fugiat sunt esse. Ut et voluptatem magnam neque reprehenderit quia provident. Quod ea in beatae quia. Omnis ut aut dolorum eveniet nisi. Iste iusto ut molestiae. Aut est nisi dignissimos a. Quibusdam aliquam qui iusto neque fugiat rerum. Unde aut voluptas velit facere. Architecto consectetur voluptatem provident. Voluptatem eos earum dolores quae et vitae. Nisi amet velit velit et a delectus quam. Ut ipsa est sint quas. Iusto dolores quia accusamus animi natus dolor sapiente. Minus doloremque dolor quae est. Omnis nihil eaque velit. Quia et earum vel porro cumque numquam totam. Qui saepe error voluptates rerum nesciunt aut minus eaque. Est pariatur sapiente eius molestias est. Velit velit et quod omnis cupiditate numquam ad et. Repellat exercitationem doloribus rem. Repellendus culpa pariatur molestiae voluptates et facere totam labore. Vel minus dolores officia velit sit est esse. Voluptatem iure velit vitae perspiciatis iste quam quia dolore. Illum nobis sed ut commodi voluptates et sed. Laboriosam distinctio dolorum itaque ipsum id quibusdam. Omnis reprehenderit dolorem omnis voluptas. Nulla voluptatem eius doloribus porro repudiandae. Et necessitatibus voluptates aut porro ut doloribus impedit. Rerum quae omnis quo cumque velit quia. Molestiae tempora quos deserunt quia id dolorum nisi. Et pariatur magnam corrupti rerum aut. Non modi molestiae repellendus exercitationem. Quia aut voluptas enim ut ut expedita id consequatur. Et veniam voluptates modi suscipit laboriosam ut aspernatur. Doloremque illo tempore quia non vel quidem unde ea. Quibusdam natus dicta ut enim voluptatem. Et reprehenderit illo non non. Alias et quia voluptas. Corporis qui non et aut voluptatem et pariatur. Distinctio voluptates voluptatem corporis suscipit. Nesciunt accusamus minus iste qui nam neque dolorem. Neque corporis aut quia iure voluptate culpa. Sunt accusantium ut fugit qui vero sapiente molestias. Repellendus atque temporibus voluptate et excepturi at accusantium. Ipsa iste possimus dolorum. Velit velit illum aliquid unde hic. Ut rem molestias qui. Reprehenderit consectetur aut commodi. Consequuntur consequuntur velit distinctio. Magnam veritatis reprehenderit eveniet qui. Ea et error in. Sit sunt qui quia. Placeat autem occaecati voluptatem. Alias et est ex eos magnam soluta ducimus dicta. Sequi deleniti voluptas ut non exercitationem dolorum. Voluptatem dignissimos qui voluptatem voluptatem aut qui cupiditate. Numquam quaerat alias qui et nostrum quo at. Repellendus sunt aut et sed. Qui ipsa perferendis accusantium rerum et eos. Rerum tenetur excepturi laborum deserunt omnis maxime aut minus. Unde ipsa non qui culpa doloribus laudantium officia natus. Explicabo optio qui quo. Dolorem odit explicabo harum aut dignissimos. Fugiat quae corrupti quaerat ut perspiciatis sed nemo fuga. Soluta porro velit tempore ipsam ut cumque. Et minus et alias animi ea. Quam debitis voluptas architecto sunt necessitatibus. Sit impedit qui deserunt et qui. Aut molestiae ut cumque quia impedit. Magni commodi sed repellat aut. Rerum voluptatem ex beatae voluptas illo ad. Eum impedit suscipit quo distinctio repudiandae. Molestiae odit reprehenderit eos quos quo ipsum expedita. Numquam nemo eveniet veritatis facere et accusamus. Tempore et et quis voluptatum eaque autem voluptate. Aspernatur nisi deserunt voluptas enim unde. Pariatur ut in maxime voluptatem qui repudiandae. Officia porro adipisci rerum temporibus. Sed labore quidem optio et sed nulla. Impedit laudantium sed asperiores unde rem debitis. Cum consequuntur reiciendis at consequatur. Laborum ipsa commodi unde sit quia alias velit. Quisquam dolor eos aliquid totam sed et. Omnis enim inventore ab. Earum est ex voluptatibus aliquam aut. In rerum autem et quidem perferendis expedita. Fugiat minima id est aut. Sed nemo in fuga et quo iste. Nemo possimus mollitia sint rerum et beatae omnis. Eveniet est sunt nulla excepturi et. Similique ipsa perspiciatis hic ducimus enim. Laborum sint tempora corporis ut laboriosam dolores qui.', 7),
(7, '2025-02-13 00:47:38', '2025-02-13 00:47:38', 'Mr. Devon Douglas PhD', 28, 'Incidunt tenetur asperiores consectetur consequatur non dolor nemo. Sunt corrupti at nulla omnis. Voluptas error reprehenderit et consequatur doloribus unde. Repellat deleniti et et eveniet voluptatum eaque eveniet aliquam. Distinctio ducimus expedita qui deserunt maiores. Asperiores qui aut totam. Est non quia eum quod. Voluptatum qui repellat aut accusamus consectetur adipisci. Consequatur assumenda expedita soluta officiis alias quos. Dolorum sunt necessitatibus qui perferendis recusandae voluptatem. Temporibus aspernatur odit velit illum ducimus. Qui nostrum reprehenderit molestiae enim. Sed delectus numquam voluptatem nobis minima. Quod eius est voluptate nulla vero velit. Suscipit dolorum modi totam corporis. Quod iure eos tempora ratione sed. Dignissimos laborum blanditiis et sed error. Consectetur exercitationem ut voluptas est voluptatem deleniti qui illum. Odit ut et quo eaque. Culpa quasi laudantium fugit. Debitis similique et saepe enim totam est odio. Soluta blanditiis totam doloremque. Nobis doloribus saepe id nihil quo quibusdam. Et repudiandae aliquid cupiditate ut nesciunt nobis esse. Et ut sint deserunt repellendus dolor molestiae quia repellat. Sint iure voluptatem nobis ut optio rerum. Ut rerum et laborum est non magnam sunt. Veniam at rerum illo molestiae. Dolor enim architecto unde consequatur. Est modi dolorum nostrum harum. Sequi eius unde voluptatem nesciunt a deserunt. Beatae est asperiores consequatur repellat ea. Asperiores accusantium unde optio nihil nesciunt. Incidunt eaque soluta suscipit est sunt tempore et placeat. Beatae ad provident aut est dolorem voluptatibus sint. Expedita cumque error et laborum nam voluptatem distinctio maiores. Architecto rerum asperiores voluptate laudantium ducimus enim. Et id molestiae ab maxime ut. Asperiores velit odio harum autem quia ex. Ratione modi suscipit voluptates voluptatum. Qui maxime odit molestias aut. Quia aut est quia. Ullam facere quis officiis aspernatur. Alias consequatur iusto ut. Impedit ut rem distinctio dolorem recusandae sapiente ab. Quos eum quidem iure in voluptatum temporibus. Recusandae tenetur aut aut aut nesciunt esse. Eum quidem quisquam ea consequatur earum quasi. Dignissimos exercitationem architecto esse ut corporis tempore. Est dicta dolor amet adipisci dolor. Et eligendi saepe dolor ea. Ea esse tempora cum. Cum pariatur voluptas nobis laborum ab. Autem sed amet numquam id. Molestias suscipit reprehenderit deleniti odit saepe voluptatem. Quae quaerat non nulla quisquam vel eius laboriosam. Est facere consequatur ut voluptas rem officia molestias. Deserunt pariatur nisi ut sed. Incidunt et sit dolorem sint nostrum eos. Sit fugiat ullam corporis unde saepe omnis. Ipsa fugiat facere consequatur temporibus autem aut aut nulla. Nam laboriosam modi voluptatibus et soluta. Soluta consequuntur quas ab harum. Rem similique odio aut consequatur veritatis nihil dolore rerum. Ipsum dolores nulla officiis illo voluptas modi.', 9),
(8, '2025-02-13 00:47:38', '2025-02-13 00:47:38', 'Saul Nolan', 59, 'Distinctio et et amet reiciendis dolorem et. Doloremque laudantium exercitationem provident doloremque cupiditate dolor. Enim aut molestiae neque rerum tenetur doloribus facilis. Et modi modi et numquam. Voluptatum dolores et sit omnis et illum. Dolore sunt ipsa velit et quis perspiciatis aspernatur. At vel asperiores in accusamus qui rem nulla laborum. Temporibus rerum ducimus dolores accusamus. Et praesentium voluptatibus necessitatibus. Vel est veritatis nobis rem est possimus quisquam. Sed quibusdam enim rerum voluptate magnam aut quia aspernatur. Officiis maxime eum et. Eaque dolores quia quia hic facere. Modi temporibus laborum dolores amet quo nemo. Aut ut quaerat voluptatem id odio nostrum. Dolorum et eligendi ducimus voluptatibus eum. Voluptas explicabo omnis nostrum. Ea quia autem beatae odio. Aut est libero et vitae ipsam unde temporibus. Ea earum eligendi quibusdam. Ad reprehenderit qui labore officia aspernatur. Distinctio omnis facere amet omnis omnis. Culpa quia quibusdam qui tenetur distinctio. Qui voluptas enim reprehenderit quasi. Ducimus nihil libero ad qui. Placeat neque quia quos corrupti aut modi. Eaque vero asperiores non laborum. Consequatur voluptatem aut ea voluptate quasi quis et. Qui officia sequi omnis nulla vero atque dolor. Hic mollitia nihil molestias ut. Ad quos sequi veniam qui amet. Facere ea voluptatibus dolores sed dicta provident. Beatae non sunt nam eos ex. Inventore fugit expedita commodi consequuntur blanditiis reprehenderit. Aperiam quo voluptate asperiores dolorem id qui. Dolorum quos sit nam et aliquid quia laudantium. Ad illo deleniti atque. Saepe quisquam consequatur necessitatibus doloremque voluptatibus aliquid. Voluptatem quo distinctio velit possimus. Dolor aut corporis est debitis aut. Recusandae quia facilis quis fuga dolor sit. Quaerat temporibus et ipsa illo nam qui molestiae. Quis consectetur doloremque officia assumenda. Aut repellendus nisi et. Alias nesciunt et officia et. Accusantium tenetur quo eum modi qui ab. Omnis tenetur tenetur voluptate reiciendis. Praesentium a blanditiis ad praesentium temporibus voluptates sunt. Distinctio ipsam itaque quia id aspernatur. Beatae praesentium id quam fugiat expedita architecto praesentium. Et rem dolore autem et. Consectetur illo error eaque ullam. Vitae autem consequuntur ut. Ipsam voluptatem odit provident dolores ab. Aut optio consectetur ratione eum voluptatem quo sit. Enim reiciendis praesentium aut et velit minus. Excepturi inventore est enim. Repellat ex est provident atque et dolor omnis. Omnis corrupti aperiam provident consequatur consequatur. Doloremque placeat minima natus impedit dolor in. Assumenda eveniet at ea ex. Deserunt possimus velit sequi harum qui necessitatibus quia. Molestiae laudantium a ipsum ducimus. Sunt sit molestiae aut fugit sit facilis accusamus. Quae illum veniam voluptatem doloremque deserunt aperiam. Aut omnis quo eos laudantium. Animi et perspiciatis numquam. Omnis quam nostrum ea qui sint. Ipsa qui harum facilis tempore beatae et. Repudiandae voluptas autem labore odio. Nobis laborum nulla aperiam nesciunt. Architecto nam velit ab suscipit repellat sint est et. Sit asperiores consequuntur illum facere. Est ut illum ipsum rerum enim. Aut recusandae ut quia molestias. Quia doloremque error non sed nostrum molestiae. Non et molestias omnis et voluptas sed. Perspiciatis sapiente qui labore est non ducimus. Ipsa quasi et rerum iste qui quaerat culpa. Illum autem ut in architecto deserunt. Voluptas dignissimos eum doloribus consequatur blanditiis. Temporibus voluptatum incidunt excepturi facere dignissimos. Dicta tenetur nulla quaerat nobis iste et dignissimos. Voluptatem sed fugit blanditiis ut et velit. Optio aut eos quia est sapiente minus facere. Itaque et sunt enim et quas sit voluptas aperiam. Dolor sunt ullam vero doloribus et quidem nesciunt. Ipsa dolor possimus et eveniet dolorem rerum et. In omnis voluptatem aut. Non quia dolores alias aut. Rerum et ipsam praesentium in qui. Assumenda esse tempore aut atque deserunt fugit. Est atque eius voluptas necessitatibus pariatur sed velit. Magni et ducimus velit quod et quisquam. Eos aut illo sed. Enim earum perspiciatis ea rerum mollitia. Laboriosam eum non eos ut deleniti temporibus. Omnis maiores et iure voluptatem dolores quisquam. Consequatur molestiae eligendi nulla qui autem non. Maiores numquam nihil molestiae quia asperiores autem praesentium. Maxime rem nobis quos rerum sunt exercitationem rerum repellendus. Id repellat modi optio est. Perferendis aliquam quia voluptatem vitae molestias nihil enim molestias. Sed ratione corporis vitae voluptas eveniet. Vel et est et. Minus non quasi quasi blanditiis corporis et voluptatibus. Tenetur nulla tempora amet. Qui aut officia non magnam. Earum labore animi eum quaerat veritatis et corrupti. Nesciunt ut ut a ea eos esse. Velit labore est ut est qui est.', 2),
(9, '2025-02-13 00:47:38', '2025-02-13 00:47:38', 'Gerald Quigley', 44, 'Doloribus est et consequatur eius corrupti. Eos odit id voluptas ex exercitationem sit. Nostrum totam atque possimus nostrum corporis laudantium beatae deleniti. Iusto similique magni adipisci reprehenderit dolor repudiandae. Laborum dolor quasi sit quo vel dolor et omnis. Ipsum saepe eos error tempora dolor. Qui aut sit esse quaerat. Aliquam et repellendus eos accusantium ab quod. Quaerat est earum voluptate ipsum. Dolor porro commodi officia quia autem sapiente. Quaerat vero quidem adipisci ad. Ad voluptas quia similique voluptatibus. Non qui voluptas rem quisquam officia voluptatem. Tempora enim rerum dolorem natus vel reiciendis. Natus libero accusantium asperiores quasi. Voluptate in numquam aperiam consectetur. Earum recusandae ex aliquam fugit est est et illum. Ut dolore quod omnis laudantium sunt voluptatum. Ratione neque itaque porro assumenda iste eveniet. Non architecto neque ipsam iusto tempore. Accusamus deserunt qui qui modi. Molestiae quaerat aut inventore inventore quibusdam voluptas. Est illum est aut dolores id. Libero eos natus quia voluptas et sed autem dolorem. Quasi saepe autem modi sint explicabo facere aperiam. Aut eius omnis enim non unde necessitatibus laborum. Delectus vel incidunt quam exercitationem. Illo sapiente quis molestiae quibusdam. Cum ut aut ratione et eligendi neque nostrum. Accusantium beatae asperiores asperiores eius minima. Vitae inventore quasi eum iste et. Soluta quia odio quis quaerat soluta sit. Voluptas quod reiciendis dicta mollitia neque. Enim nisi dolorem non similique non et dolorem. Rerum enim et quia. Voluptatem quisquam ut vero corrupti. Voluptas accusamus dolore qui accusantium. Nulla vel reiciendis beatae laboriosam. Et eos id nesciunt voluptas placeat tempore quo. Asperiores esse voluptatum ut vel saepe. Odit et et aliquam veritatis. Facere alias qui blanditiis fugit dignissimos in adipisci. Voluptate ducimus et eos voluptas omnis id. Consequatur dolorem sed ut corporis voluptas. Quis nobis et dolor est repellat temporibus dolorem quos. Tempora alias architecto fugiat rem deserunt iusto. In debitis officiis harum quis est voluptate qui. Ratione maxime ratione iure consequatur cupiditate assumenda. Quia dignissimos voluptatibus assumenda eum praesentium. Voluptatum sint dolorem quae alias sequi in deserunt. Rerum corporis ea laboriosam fuga consequatur est. Architecto hic ipsam cum assumenda doloribus. Vitae est minus et est est commodi expedita. Unde occaecati non quo dolores. Facilis et molestias nobis et delectus excepturi ab quos. Molestiae similique molestiae consequatur neque expedita maiores ut ipsum. Provident veritatis nam dolorem consequatur quibusdam sint est. Eveniet ut eos fuga sed qui quia officia porro. Qui velit laboriosam eius et. Consectetur iure sunt in repudiandae dolor at illo. Velit vitae impedit dolore corporis voluptatem error. Natus quaerat atque non molestias aut. Aut assumenda possimus necessitatibus impedit vel. Harum veritatis occaecati adipisci non enim aspernatur non. Exercitationem tempore tenetur sit ullam. Non saepe autem quaerat tempore. Illo officia earum voluptate voluptatum aperiam voluptatem. Voluptate voluptatibus consequatur quidem commodi. Eum aperiam nemo et nemo eum. Labore omnis est quasi voluptatem soluta. Delectus ad voluptatem rerum. Saepe adipisci nihil nam soluta dolores nobis. Repellendus nobis minima ratione magni rerum cum nulla. Itaque molestias repellendus unde consequatur. Esse qui magni ut rerum ea suscipit. Deleniti unde similique distinctio nisi sed. Ad commodi eos aut in repellat. Est eos aspernatur aut. Excepturi dolor qui molestiae explicabo possimus sapiente autem aspernatur. Illum quia consectetur cumque exercitationem. Dicta debitis et accusamus odio. Quis eum deleniti est sit nesciunt. Hic deserunt nemo omnis consequuntur perspiciatis fugiat. Enim praesentium velit optio consequatur. In et reprehenderit repellat sequi voluptatibus. Quibusdam quam itaque ipsum non earum qui quisquam. Quas assumenda sed doloremque sed. Illum eum alias quo mollitia placeat nam eos. Quia blanditiis similique culpa ipsam. Veniam sequi sit ut non temporibus. Aut aut veritatis vel rem aut. Quos eveniet magni officiis libero quia. Qui voluptas quo est asperiores atque. Molestiae consectetur blanditiis consectetur quidem minima delectus.', 2),
(10, '2025-02-13 00:47:38', '2025-02-13 00:47:38', 'Dr. Art Dare', 25, 'Rem ea dolorum dignissimos vel quisquam tenetur et. Blanditiis qui nemo molestiae quibusdam tempore. Numquam perferendis sunt unde dignissimos saepe. Velit iusto in voluptatem similique sequi qui tempore. Et quia aspernatur ut quia sequi ipsum cumque accusantium. Et amet aspernatur amet. Itaque nemo perferendis consequuntur. Quia non consectetur voluptatem consequatur quo voluptatibus. Accusantium facilis ab omnis in et. Necessitatibus accusantium cumque eaque eos ut culpa. Nihil voluptatem similique ut est non et suscipit. Esse porro ad ex nostrum adipisci qui aut nulla. Dolorum et id delectus et quaerat ipsum tempore. Fugit quo perspiciatis provident repudiandae. Officia unde asperiores qui dolores. Accusamus voluptas dolorem nihil consequuntur. Non distinctio et omnis deleniti quos inventore officia. Dolorum in minima ut quaerat perferendis quis. Omnis quas praesentium quis nisi consequatur. Quos reprehenderit sed non totam nihil. Nostrum voluptas neque pariatur qui deserunt optio quas qui. Ullam velit eligendi voluptatem. Cupiditate dolorem totam natus et. Consequuntur perferendis rerum commodi necessitatibus facilis. Est sequi id suscipit nobis et occaecati incidunt velit. Est quidem magnam iure et officiis quo non. Consequatur odit facilis facilis corporis excepturi. Magni fuga accusantium quae vero et accusamus. Nemo accusamus reprehenderit eaque maiores quaerat unde. Illo et quo doloribus. Modi placeat officia quas rerum. Et aliquam magni dignissimos quia dolor. Quae aut est non nesciunt eum velit. Voluptates minus possimus est. Est vero aspernatur quod odio omnis omnis sapiente. Itaque animi possimus fugiat eaque. Ut reiciendis sunt iusto tenetur numquam consequuntur. Non fuga non repellat iure ut enim. Nostrum eaque quos dolor libero enim. Voluptatem incidunt libero quaerat ipsum alias. Adipisci non hic eius quae neque ut et. Praesentium qui soluta dolorem labore temporibus aut quas. Consequatur voluptas placeat quisquam dolor. Atque quaerat id dolores molestias. Pariatur quo enim perferendis aperiam. Voluptas repudiandae accusantium ratione possimus error. Recusandae quos necessitatibus reprehenderit quis rerum. Consequatur sed sit eos libero. Officia delectus quis temporibus et sed. Repudiandae fuga voluptas in debitis fugit reprehenderit aliquam qui. Libero est consequatur unde ipsam laboriosam consequatur. Culpa voluptates quidem ea harum minima eum sed voluptatem. Laboriosam possimus laudantium sunt enim. Tenetur praesentium consequatur officiis rerum repudiandae et veritatis. Qui enim atque id consequatur voluptas doloremque nihil. Qui quia magni debitis expedita. Rerum explicabo tenetur vel quibusdam vel. Modi adipisci exercitationem alias dolorem eius facere. Inventore consequatur dolor et. Voluptas natus labore nesciunt. Commodi sit debitis fugiat voluptate aliquam. Totam nemo voluptate voluptates totam est at rerum. Officiis ipsa quaerat eaque qui numquam. Iure et sit non omnis aperiam. Dolor qui vel dolorum tenetur corrupti voluptatem. Ea debitis dolores ex ducimus atque. Vel dolor quibusdam et suscipit. Voluptatem provident repellat quia veniam alias ipsum ab. Facere fugiat recusandae numquam expedita. Recusandae in commodi qui quas. Nemo cupiditate occaecati qui dolores est. Minima voluptas optio sit eum quisquam id. Quo et quasi voluptatum quia modi. Non excepturi et sint laborum. Mollitia eligendi fugit qui repellendus sequi modi eos dignissimos. Aut nam non nobis autem velit. Explicabo consequatur quas assumenda magni qui sequi. Minima deserunt enim dolorem harum. Aut non tempora dolorem est qui reprehenderit. Saepe nobis et sint nostrum impedit aliquam fuga. Et aliquam corrupti aut. Reprehenderit qui sint veritatis accusamus sit eum laudantium. Velit autem ad asperiores doloribus. Dolor autem modi libero non voluptatem et quis. Culpa nesciunt doloremque aliquam omnis quia. Unde iusto dolores ea pariatur. Et adipisci quia qui repudiandae laboriosam molestiae praesentium non. Facere ea perspiciatis enim. Dolorem nihil ipsam aut ut voluptatibus. Iste provident sed in sed voluptas et sequi. Amet quaerat enim iste excepturi optio. Voluptatem est et ratione blanditiis molestiae in rerum. Mollitia aut voluptas animi voluptatem est. Molestiae distinctio sed id repellendus dolor dolores. Accusamus ab itaque aliquid reiciendis numquam. Est dolorem quo voluptas doloremque illum maiores.', 5),
(11, '2025-02-13 00:47:38', '2025-02-13 00:47:38', 'Tremayne Baumbach', 33, 'Laborum omnis aperiam voluptate sapiente. Tempore eum repellendus est eligendi. Et labore impedit ut occaecati sapiente reprehenderit et quo. Aperiam quis quibusdam quia officia et accusantium id. Qui reprehenderit distinctio dolorum consequatur iure dolore quidem qui. Enim aliquam repellendus laborum vitae est. Laudantium quae ducimus quaerat recusandae fuga provident recusandae. Et est qui sit voluptas. Autem blanditiis perspiciatis autem quis. Sed delectus et quas vel eum ducimus nesciunt recusandae. Harum autem recusandae impedit sed iusto maxime provident. Dolores vel dolores vel tenetur et quidem ipsa eum. Repellat eum maxime dolore voluptates debitis. Voluptas mollitia natus sint ut quia dignissimos qui. Dignissimos voluptatibus totam voluptatum minus. Veniam id hic numquam molestias labore. Molestiae libero error esse sed. Voluptatibus recusandae voluptates laboriosam quod nemo qui dolorum. Quis consequatur ut et eos aut voluptatem non. Inventore expedita eius tempora velit nisi. Qui illum qui deserunt. Autem eum harum consequuntur exercitationem quaerat veniam a. Neque odio quo ut et vel consequuntur. Error voluptas adipisci maxime iste ut vel. Omnis commodi et tempore quod beatae labore. Neque doloremque vel commodi sunt necessitatibus esse. Reiciendis aliquam deserunt totam molestiae sit quisquam. Nihil veniam quia delectus eveniet mollitia laudantium et. Fuga nostrum doloribus et voluptatum ipsa facilis. Ut eos ea ipsam aperiam possimus. Expedita laudantium voluptatem beatae minima. Maiores id voluptatum aut excepturi. Consequuntur facilis molestiae voluptas cupiditate nisi. Odit similique quo nisi dolore. Nostrum optio fuga at autem et. Aut ea cumque et. Exercitationem nam in autem porro omnis odio qui sit. Et officiis suscipit vel. Debitis laborum tenetur adipisci corrupti non aspernatur ut. Consequatur placeat beatae eveniet rem alias eum fugit. Voluptatem quia non velit facilis. Qui iusto id vitae molestiae sed. Voluptatem qui exercitationem voluptas qui voluptate voluptas. Est enim esse et rerum deserunt quae possimus dolores. Qui autem doloremque error aperiam dolor et aspernatur. Aliquid id est possimus quo itaque molestiae eveniet. Totam hic iste quo quis quis dolor. Quia veniam harum odit. Delectus optio expedita et neque velit. Voluptatem et eum dicta. In impedit eligendi voluptas numquam voluptatem omnis. Adipisci qui fugit et nesciunt qui quam. Voluptatibus sint nostrum et alias assumenda autem aut earum. Corrupti quos et ea excepturi consectetur quibusdam nisi id. Expedita facilis voluptas laborum id. Voluptatem aspernatur debitis velit eligendi officiis excepturi. Et saepe facilis quidem eum sed deserunt. Aut et voluptate et dolores omnis iusto. Et officia numquam repudiandae repudiandae consequatur dicta. Quo tempora non doloribus beatae quibusdam voluptatem qui. Omnis molestiae cum qui consequatur explicabo sed voluptatem. Et voluptas omnis ratione assumenda doloribus. Esse iusto distinctio temporibus vitae molestiae accusantium ut qui. Facilis blanditiis corporis nulla ut cum minima. Tenetur est cumque cum minima vel odio. Et ex nobis sed cupiditate repudiandae est dolores ut.', 7),
(12, '2025-02-13 00:47:38', '2025-02-13 00:47:38', 'Norbert Barrows', 33, 'Neque animi quisquam officia a mollitia consequatur non ea. Illum nulla non sed doloremque. Voluptatibus ad et praesentium eveniet pariatur cumque assumenda. Rerum eum et ab voluptates dolor possimus vitae. Molestiae sit consequatur sint ut nisi. Expedita odio molestiae voluptas assumenda enim vel. Aspernatur a et nam cum enim culpa. In voluptas soluta et eos assumenda. Cum laudantium repudiandae sequi officia dolores rerum ex. Suscipit non tempore et veritatis animi. Eveniet corrupti tempore voluptate sapiente quia aliquid est. Veniam incidunt in adipisci quod inventore deleniti. Natus nemo debitis qui perferendis quia qui dolor. Ut qui et quo nihil. Et necessitatibus alias quis. Sint excepturi ipsam doloremque cupiditate dolor. Distinctio odit veniam quis cumque ea. Qui fuga earum ut sit. Enim iste id sed beatae et voluptatum. Qui rerum et sint et mollitia eum. Et placeat natus incidunt ullam cupiditate labore. Maxime saepe ut adipisci adipisci sunt. Quos unde sapiente dolorum id in. Iure qui excepturi minus quisquam tempore. Blanditiis modi iste doloribus rem nemo. Quia ipsum corrupti voluptas non incidunt sint assumenda. Aperiam fuga id temporibus voluptatibus impedit. Dolorem ut qui ut facere aut. Reprehenderit voluptatem quia qui autem non omnis. Quidem sint suscipit perferendis sunt omnis qui quo. Rerum quis qui et corrupti. Qui enim vitae modi est non labore quod enim. Aliquam qui veniam et natus dolorem officiis sequi. Aut ab deserunt ut culpa ut consequuntur. Vero culpa doloribus dolore sed at sed esse. Debitis modi vitae eum velit voluptatem velit est. Quia odit omnis omnis ea porro rerum expedita. Ut assumenda libero maxime dolorum quod iusto natus. Et recusandae pariatur dolores consequuntur natus. Repudiandae quae et qui optio doloremque. Reiciendis voluptates delectus ad nulla animi dolor. Eveniet nam laudantium sed non. Aut qui ut autem itaque eum. Porro nam distinctio neque fuga. Beatae impedit amet qui voluptate quis. Mollitia distinctio molestias est qui soluta. Aut ab nobis sunt adipisci. Enim nobis ut ut occaecati quia porro. Modi nemo illo provident quis. Consectetur omnis totam deserunt a tempora eaque molestiae. Consequuntur ea explicabo sint quia molestias. Non odio qui voluptatibus unde rerum neque. Inventore sunt vitae pariatur earum vero magni non. Possimus repellendus similique iste omnis quas saepe. Quis quia laudantium quam. Est eum amet dolor porro eaque ut porro. Doloremque distinctio sed sequi quod et. Placeat ut minus sequi libero nulla sit. Qui debitis assumenda voluptatibus quo quis sequi sapiente dolorem. Qui consequatur dolores tempore. Laudantium accusantium debitis hic vero voluptas dolore natus. Delectus odit repellat doloremque reprehenderit est. Vel numquam culpa et excepturi molestias et ut. Blanditiis velit aliquam quo quia nihil. Fugiat reprehenderit dolores doloribus unde laborum. Omnis accusantium autem in et velit similique. Quaerat saepe eaque perspiciatis nihil doloribus. Et possimus omnis doloribus earum. Repellat illum nobis ut odio quia voluptatem. Ut debitis harum dolores magnam et officiis nobis. Officiis sit perspiciatis commodi hic ab. Nostrum ipsa commodi ducimus non dolorum omnis expedita. Iusto at non praesentium eos iure. Doloribus quia consequatur velit adipisci et impedit quia voluptate. Qui aut ullam quia quibusdam ab sunt a voluptatum. Necessitatibus ut quia quo voluptas ut. Sit sint occaecati aut est aut nam. Non voluptatem pariatur nostrum molestias voluptate. Eum iure sapiente itaque architecto cupiditate. Quibusdam qui veritatis magni accusantium sapiente rerum quisquam. Ut ut sit at vel perspiciatis dolore. Voluptas qui voluptates sed libero impedit tempore. Tempore sint adipisci odio et recusandae dolor itaque omnis. Corrupti ut impedit doloremque dolorem enim. Ut ipsum quidem nobis dignissimos omnis. Consequatur suscipit incidunt cumque tenetur quia tempora. Sed sed vitae occaecati est natus. Culpa saepe numquam tempora nostrum. Voluptatum laudantium laboriosam totam qui magni. Numquam quia et sint enim corrupti omnis. Eius qui asperiores et reprehenderit. Et aut cumque ducimus a. Non cum voluptate qui accusamus. Tempora expedita non quia praesentium enim voluptatem. Laborum reiciendis velit maxime minus. Ducimus nesciunt illo quia reiciendis atque repudiandae rerum. Id repellendus perspiciatis eius accusamus repellat eum. Facilis dolorem consequatur omnis eveniet suscipit voluptas. Sunt dolore quia maxime. Delectus numquam voluptatibus enim incidunt quam neque. A adipisci unde quas voluptatum voluptatem. Alias a ratione alias nulla autem consequatur ut. Et ratione vero iure sunt iure aliquam et. Impedit amet velit sunt suscipit provident ut. Velit ut officiis ut officia. Provident illum quo officia itaque provident occaecati et. Eos necessitatibus omnis reiciendis occaecati quo animi dolorum. Non sapiente eum itaque omnis in illum. Quasi sunt nulla nam illo temporibus natus. Et et qui laudantium. Tempore debitis consequatur vel laboriosam. A eligendi id quaerat impedit nihil commodi recusandae adipisci. Aut iusto pariatur inventore culpa necessitatibus voluptates commodi qui. Consequuntur accusantium a voluptas itaque laudantium nihil qui. Dolor non expedita sit consequatur debitis assumenda aperiam adipisci. Nostrum hic voluptas eaque. Id inventore ea ut vero fugiat soluta aut voluptas. At quam cumque at non. Nesciunt et velit ex ipsam quos et voluptas. Doloremque modi libero eius dolorem quia magni et. Aut inventore asperiores voluptatum ut vel sit numquam. Inventore et voluptates dolor fugiat. Unde qui nobis qui nesciunt. Et necessitatibus est nihil cumque. Eius quae voluptatem rerum voluptas. Cumque fugit qui neque ut. Magnam at est a. Ipsam debitis expedita eos officia repellat. Rerum pariatur et et saepe voluptates consequatur ipsum. Minima sed culpa et et mollitia non. Fugit quia blanditiis animi illo voluptate.', 3),
(13, '2025-02-13 00:47:38', '2025-02-13 00:47:38', 'Prof. Bill Pouros', 56, 'Aut magni consequuntur hic pariatur sunt. Corrupti ab eveniet id voluptate sunt cum. Sit odio quo dolores tempora autem architecto. Eveniet consequatur placeat qui quae enim. Vel eum omnis id omnis sunt ad veritatis. Recusandae similique incidunt totam et impedit at recusandae. Atque voluptatem sed aut ut. Qui officia repellendus quidem rerum. Accusantium voluptate illum nihil sunt voluptas aut. Modi saepe nemo ullam et fugit mollitia. Autem ut veniam at minima at ut recusandae. Cupiditate ut dolor ipsam numquam exercitationem sit repudiandae aperiam. Sint non ipsum dignissimos illum reprehenderit dignissimos nobis. Aut nulla et est aut delectus. Earum explicabo accusantium quasi quam. Odit deleniti facere qui consequuntur repellendus rerum quia. Aut consequuntur delectus ducimus. Incidunt nulla et ducimus deserunt. Earum aliquam aut labore ipsum cupiditate minus non. Occaecati debitis sint ipsum. Sint tenetur fugiat rerum aut. Quae occaecati quibusdam ab sunt aliquam tempore laudantium iure. Et aut voluptatem illo eveniet. Exercitationem maiores corrupti enim ut adipisci amet. Est sunt eaque nobis enim enim debitis ipsum. Ratione sint molestiae est possimus sed libero repudiandae. Ut aliquid voluptatem quidem veniam nisi repellendus dolores. Voluptate dolorem alias quaerat molestias sit rerum. Expedita et ducimus autem ea ut. Cumque reprehenderit qui odio inventore est repellendus aut. Alias inventore facere in possimus qui doloribus. Ea ab sed nobis sed est recusandae. Totam quasi eveniet tenetur sint nisi distinctio. Ad quia ea et quia. Similique quisquam eos omnis eum dolor natus impedit nobis. Aliquid consequuntur saepe totam rerum. Odio molestias velit omnis aperiam error voluptatibus beatae sunt. Architecto ea dolores esse consequatur. Optio assumenda similique eveniet. Dolores et debitis cumque consequatur veniam. Architecto iusto non non adipisci ad velit. Dolorum laborum eaque culpa enim eligendi quos rem. Id numquam pariatur quod odio aliquam. Fuga libero rem eaque quis iste nihil cumque. Explicabo provident asperiores dolore architecto molestiae aliquid enim. Mollitia ad est omnis qui quos aut. Nesciunt dolor ad vel maiores consectetur repudiandae nihil velit. Numquam saepe dolorem nihil tempora magni autem animi dolorum. Praesentium soluta perspiciatis placeat alias. Deserunt id explicabo fugit blanditiis alias. Minima ut vero omnis quas doloribus saepe culpa. Sequi voluptatem ut repudiandae explicabo voluptas tempora officia. Eveniet aspernatur nam harum voluptas sed. Quis similique corporis repudiandae aut perspiciatis nesciunt. Magnam enim aut eos qui laborum et voluptate. Distinctio ea hic nulla temporibus et voluptates rerum minus. Eaque laudantium voluptas doloribus saepe. Eius ex fugit modi aut ut. In consectetur vel officiis. Unde sit cumque rerum voluptatem consequatur incidunt at. Consequuntur impedit voluptas ea quo asperiores sed. Repellat facere ex at earum. Aut est sed ea qui quod eius commodi. Voluptate atque vero ut quia sit tenetur mollitia nisi. At recusandae molestiae occaecati dolores. Cum alias sit illo vero officiis impedit. Voluptatum fuga repellendus dolorem ut qui ut provident. Est adipisci sit doloremque beatae. Accusamus corrupti et molestiae ut aut qui. Voluptatem molestias laudantium ducimus. Rem nisi sapiente eligendi ut eos voluptas voluptatem. Voluptatibus ut enim inventore. Molestiae architecto id ratione et eum. Aut ut ut ratione quod dolor qui nihil. Quasi dignissimos voluptatum ut. Ratione itaque suscipit qui et voluptatem voluptate autem. Et quos molestiae eos qui dolores. Maxime fugit laudantium iusto ut atque. Accusantium sint autem dicta corrupti. Quasi consequatur et voluptas molestiae repudiandae. Dolorem tempora sit magnam non molestias. Sint quibusdam non velit sunt. Soluta eligendi itaque ipsam sed tenetur. Iure numquam ratione ut non velit ea. Ullam alias laboriosam minima ducimus reprehenderit. Ut earum sequi rerum magni. Voluptatem voluptate quia qui dolorum numquam. Sint laboriosam laboriosam at laborum mollitia. Ut qui qui inventore laudantium incidunt laboriosam unde nihil. Laboriosam a cupiditate ex quia suscipit molestiae. Vel quisquam eum adipisci iusto. Magni dolorum voluptatem recusandae atque occaecati molestiae omnis. Modi consequatur facere incidunt facere inventore eum. Vero nemo laudantium magni. Eligendi ab nostrum occaecati cum dicta autem fuga qui. Ab rerum quidem ut sed et. Natus dicta sed optio eligendi. Explicabo nam maxime natus officiis impedit. Omnis enim et rerum cupiditate ipsa. Accusamus consequuntur molestiae non possimus dignissimos doloribus ipsa. Maiores ut quasi dolor. Porro vero aut illum optio vel inventore reprehenderit. Quam qui quia fugiat voluptates consequatur. Eum voluptatem voluptatibus ea nihil minus occaecati impedit. Incidunt enim sapiente vitae minima. Perferendis aut hic nam qui sit minus dignissimos. Ipsa minus deserunt pariatur animi. Cumque aliquid exercitationem ab et accusamus cumque soluta et. Mollitia eos ut quidem labore quis. Officiis voluptates minus sequi sequi blanditiis hic. Quia ut quam quisquam.', 1),
(14, '2025-02-13 00:47:38', '2025-02-13 00:47:38', 'Tanner Feest I', 61, 'Ut laudantium nihil aliquid et dolor rem. Eaque suscipit est distinctio eligendi nam quia. Dolorum ullam sint vel excepturi sequi. Aut et rerum nostrum quas est quos nesciunt. Et quasi ex velit dolorum harum sint aut. Corporis est quis expedita nam aut amet velit. Vero vel veniam qui impedit incidunt aliquam blanditiis. Consequuntur doloremque sequi voluptatum aliquid nam provident. Ipsum rerum quibusdam doloremque deserunt cumque corporis. Delectus officiis repudiandae alias distinctio. Soluta quasi eaque sunt laudantium. Consequatur asperiores dolores ullam nobis ut. Placeat vitae ex inventore culpa expedita et repellat distinctio. Repellendus doloribus voluptas voluptas porro consequatur facilis. Qui facere qui vel molestiae laborum et aut. Nulla doloribus sit doloremque excepturi. Error sunt quisquam minus suscipit impedit magni. Dolores commodi assumenda delectus nam mollitia corrupti neque qui. Eos doloribus odio commodi voluptatem nihil. Suscipit dolorem ipsam vel autem officia id quas. Placeat quasi assumenda consequatur recusandae unde officiis saepe. Consequuntur cum velit modi quidem est sed recusandae rerum. Possimus pariatur hic consectetur dolorum. Excepturi qui eos reprehenderit in alias. Aut minima est nam. Ea harum non ut repudiandae et vel. Non sunt quisquam quibusdam est id veniam. Exercitationem numquam beatae ex sit. Molestiae dolore et beatae nulla ducimus. Numquam rerum qui sit dicta hic dolorum quod. Consequatur repudiandae illum at qui libero autem. Dolore vero cumque commodi consequatur est. Et neque harum sit provident. Quis tempora repellat cupiditate qui et eius iste. Id voluptas eos blanditiis quas ut. Nesciunt sit optio voluptas omnis. Laborum ab enim at error commodi animi. Temporibus est et reprehenderit aut quaerat facilis provident. Reiciendis et sint est vel sint. Ut quas vero ratione sint. Reprehenderit hic et id placeat sit id. Sint nihil amet unde non molestiae suscipit delectus. Quo et quia vitae quam qui rerum sit rerum. Inventore veniam in nemo ea quia dolores dolore. Omnis consequuntur modi explicabo et. Perspiciatis quas omnis qui quo totam qui non. Facilis rem non accusamus accusamus. Repudiandae unde dolor tenetur quia ab fugiat. Fugit nisi esse qui laboriosam. Et mollitia quis harum alias et quae. Quae earum magnam dolores odio dolores. Nemo omnis velit aspernatur et aperiam voluptatem exercitationem. Facere asperiores aliquid maxime. Magni recusandae cumque sunt quae. Culpa ut ut aliquid maiores. In modi veritatis et perspiciatis. Explicabo quod velit unde eius eos inventore. Delectus quo quis exercitationem dolor minima. Voluptas officia consequatur molestiae dolor. Aut praesentium quo tenetur numquam. Vitae qui ipsa tempora non aliquid. Natus sunt soluta velit cumque quo officiis eaque. Libero libero nulla aperiam ab voluptatem. Sequi cumque commodi odio sint vel corrupti exercitationem. Rerum itaque consequatur minus tempora. Non doloribus ducimus esse aut atque. Iure et sit voluptas. Neque enim error sunt quaerat voluptatem id sed omnis. Eos quidem voluptate impedit molestias. Ea atque odio mollitia accusantium sit blanditiis. Et est ut reiciendis dolorum. Voluptas accusantium voluptas voluptas aut vitae. Et eligendi minus reiciendis maxime nulla unde. Itaque hic sequi accusamus asperiores. A velit ab aut quas. Optio et sint vero sapiente rerum quam. Neque quos quia voluptatum soluta esse impedit qui. Omnis sequi odit sit minima similique quos. Facilis aut blanditiis ut quibusdam omnis aut et. Quos sint hic autem maiores quo. Impedit aut totam occaecati id officia possimus libero. Ipsam laborum sit quo incidunt. Vero iure velit doloribus eos. In et possimus nobis et molestias. Nemo possimus consequatur molestiae saepe et nesciunt magni. Quia ratione aut a voluptas harum eum assumenda. Non iste enim tempora optio ullam quas. Ipsum autem vero repudiandae ut rerum. Unde tenetur ratione laboriosam ad dignissimos consequuntur. Repellendus voluptatibus explicabo officia odio blanditiis accusamus voluptatem. Quo soluta ipsam ea vero illo laudantium. Labore reprehenderit est cumque qui sed. Qui sapiente magnam eligendi iusto. Doloribus sed modi ut nihil. Et tenetur architecto quas. Architecto sint est cumque consequuntur error accusantium corrupti. Commodi consectetur aspernatur tempora vitae harum consequuntur. Officiis nisi non et accusamus adipisci et officiis. Voluptates et deleniti ut quis. Aut enim neque ipsam molestiae. Consequuntur ipsa consequatur placeat quos. Dolorem doloribus est esse libero. Rem eos dolorem quia possimus aspernatur iste nulla. Consectetur fugiat fugiat et magni laborum consequuntur. Id nulla aspernatur totam ut. Recusandae voluptatem dicta in asperiores quis. Possimus quo qui et iste iure quasi eum. Voluptatum vel nihil vel est provident natus neque. Eveniet consequatur illo nam aut. Numquam praesentium voluptatem possimus enim recusandae blanditiis aperiam. Voluptates odit repellendus quia neque dignissimos ea autem. Tenetur ab sit ab amet accusantium veniam. Accusantium totam illo et perspiciatis dignissimos tenetur amet. Excepturi adipisci iusto delectus omnis. Nulla occaecati placeat non sunt. Et quis cupiditate eum optio distinctio ea et tenetur. Explicabo itaque ullam corporis. Expedita laborum praesentium necessitatibus laboriosam aliquam corporis. Sit sed quae voluptas aut dolor quibusdam alias.', 7),
(15, '2025-02-13 00:47:38', '2025-02-13 00:47:38', 'Rodger Bogisich', 64, 'Excepturi et asperiores modi quia doloribus eum. Animi ut sint nisi. Expedita qui perspiciatis alias quasi non sint corporis. Maxime corrupti omnis blanditiis laborum. Et et aut veniam. Velit architecto et et harum minima voluptas. Repellendus non quo quasi nemo quaerat vel ex. Minima qui dolor labore modi aut fugit id. Assumenda aut fugit culpa rem et rerum excepturi consequatur. Dolorem laboriosam impedit ut rerum. Eum consequatur nam quisquam nulla. Est esse veniam numquam voluptas. Quidem minima eligendi dolorem. Ad accusamus nobis sed. Rerum et magni possimus maxime necessitatibus tempora. Excepturi qui quod et quisquam. Libero ut perferendis voluptas pariatur ducimus dolor voluptas. Blanditiis quia qui atque ipsam possimus. Aut itaque optio ea incidunt. Ut facilis qui quo. Culpa amet ab iure. Ut beatae iusto qui quia eaque. Libero sit corrupti nulla consequatur. Sit corporis voluptates dolores sed minima temporibus quo dolor. At velit blanditiis ducimus ex ut reiciendis. Voluptatem ab cumque assumenda rem cupiditate error. Cum quod inventore quisquam iste excepturi ut. Maxime totam qui ad dolorum. Eaque autem repellendus id dolor expedita laboriosam ut. Quis ducimus sit dolores aliquid beatae odit unde corporis. Atque quis ea ratione provident qui ut quis. Quas a quibusdam eaque atque delectus cum. Dolorem voluptas neque laudantium vero esse. Et commodi laudantium aut labore veniam dolores iusto quo. Sunt dolorem officia non explicabo doloremque dignissimos ipsum. Consequatur unde cupiditate voluptas esse neque. Suscipit corporis velit maxime quo facere veniam. Hic dicta quibusdam sapiente ut repudiandae ut. Ipsum iste vel fuga sit illo quos doloremque. Reiciendis minima architecto labore vel. Eius quidem corporis et quibusdam. Et enim dolor dolorem et quibusdam non. Quo non aut vitae officiis earum enim. Nisi voluptas blanditiis aliquid molestias assumenda. Quam magni veritatis aut necessitatibus soluta recusandae quisquam illum. Hic sunt cupiditate eum. Id esse veniam eaque porro laudantium incidunt est. Nemo velit voluptas dignissimos molestiae maxime sint. Aut enim perspiciatis reiciendis placeat aperiam suscipit voluptates. Eum iusto provident ut voluptas repellendus consequuntur. Velit aut eveniet ullam et cum. Et praesentium natus tempore voluptatem quia placeat et. Itaque aut ipsum odio natus. Blanditiis possimus ut quasi quo ducimus nemo odio. Vitae fugit quaerat quia nisi optio voluptatibus. Id rem minima similique est eligendi voluptas. Ipsam minus nihil sapiente odit. Id exercitationem eius quasi. Cum similique corporis est enim recusandae. Ullam laboriosam aliquid et neque sit voluptates velit. Consequatur mollitia saepe aliquam ut illo voluptatibus. Eius odio ut ullam beatae distinctio incidunt. Dolores qui dolores animi aliquid officia exercitationem. Perferendis amet eius quam veniam adipisci laboriosam.', 1),
(16, '2025-02-13 00:47:38', '2025-02-13 00:47:38', 'Shaun Baumbach', 28, 'Voluptatem velit dolorem voluptatem voluptatum voluptas occaecati. Rerum et et vitae inventore sunt sint. Earum perspiciatis et dolor dolorum. Magnam ea quibusdam eos quia est fugit. Consequatur quidem harum ad consequatur dolores omnis. Eligendi nihil esse ut id. Cumque assumenda et hic dignissimos esse consequuntur. Totam ex vitae labore esse. Dolorum corporis enim enim et quasi dolorum et. Corporis unde aut nesciunt iste quaerat. Provident vel doloremque rerum incidunt reprehenderit aperiam consequatur. Culpa consequatur et labore et sequi dolor commodi id. Dignissimos modi est error quaerat et autem. Mollitia et quis possimus veritatis perferendis ut aliquid. Ut odio aliquid quod eveniet quidem fugit quia. Et minima dolor eos dolorum. Provident error commodi atque et quo aliquid. Nemo modi ut nostrum officia ut repellat. Voluptatem quo velit quia eos. Ut animi quo dolor eos iste. Deserunt qui sit dolores at. Nam adipisci neque omnis facilis amet similique et. Asperiores illo delectus ut soluta omnis repudiandae necessitatibus. Beatae officia quibusdam earum magnam. Omnis soluta dolorum qui fugit asperiores saepe est. Et nobis molestias perferendis optio nihil quo. Ut et nesciunt animi. Temporibus exercitationem fugiat similique voluptatem nesciunt. Ab adipisci architecto ad sint id possimus labore. Error sed voluptas officia qui quidem nobis qui. Officia possimus nostrum et voluptates quia. Officia ullam atque ut iusto dolorum. Quia corrupti perferendis sed voluptas. Vero consequatur velit rerum ullam. Est dolorum nobis totam placeat quo ipsum sed. Est et neque officia molestiae magni aspernatur. Corporis ut aliquam voluptatem quis harum non. Atque ut magnam exercitationem. Ipsum dolorem dolorum repellat non quo fuga consequuntur ducimus. Et voluptas illo laboriosam sit exercitationem temporibus suscipit. Voluptas sunt alias quas debitis ex. Omnis id provident aut eum pariatur consequatur perferendis. Excepturi aut id est earum aliquam consequatur sunt. Qui repellat nam veritatis rem dolores voluptate totam. Accusamus dolor provident totam voluptatem debitis qui. Tempore est fuga enim sit aperiam reiciendis. Ab nobis dignissimos sequi id. Odio est dolores voluptas et. Saepe dolor repudiandae quae omnis hic quia. Maiores voluptas molestiae quae fugiat velit. Iure nihil sunt ut autem rem. Vero rerum qui ut sit rerum quas iusto. Incidunt beatae ab asperiores quae qui non temporibus minus. Dolores qui natus amet rerum corporis et minus. Quis repudiandae quibusdam aut eum ea labore possimus. Et necessitatibus aut est distinctio. Et odit nihil fuga aspernatur placeat autem assumenda. Animi autem doloribus sit ullam error dolore. Recusandae et sequi veniam nihil rerum. Accusantium tempore earum possimus facere adipisci eos. Et autem at omnis natus non. Sapiente voluptate possimus quaerat blanditiis sint. Cumque et quo tempore ratione.', 3);
INSERT INTO `workers` (`id`, `created_at`, `updated_at`, `name`, `age`, `bio`, `office_id`) VALUES
(17, '2025-02-13 00:47:38', '2025-02-13 00:47:38', 'Dr. Jaleel Breitenberg', 23, 'Qui beatae ut necessitatibus sapiente voluptas tenetur. Sed ut similique est. Aut dolorem tenetur voluptatem sed blanditiis autem sit. Quo error sapiente illum quae iste. Natus ducimus et ab omnis recusandae aut ea quo. Ut molestiae non beatae ipsum. Est officiis quisquam provident eos corporis numquam voluptatem. A consequatur ipsa nobis. Delectus occaecati maiores ea ut necessitatibus. Ut minus delectus delectus perspiciatis vel. Dolor et maxime facere. Ex ut voluptate omnis nemo qui quidem quo est. Maiores amet sed accusantium est non. Nulla expedita sint saepe minima. Consequatur culpa ut quia alias iusto. Delectus mollitia ad rerum quidem dolorem pariatur. Dolorum minima natus ex et qui culpa nam. Quaerat voluptatem quibusdam laboriosam accusamus totam rerum quam. Et omnis culpa consequatur hic excepturi eum qui autem. Saepe voluptatum similique cumque ea aperiam harum voluptatum. Id quae doloribus voluptatem itaque et labore repellendus. Quisquam qui magnam qui consectetur. Quo qui sequi dolores fugit sint. Sequi architecto quod possimus blanditiis adipisci quia quisquam laborum. Rem perferendis ullam neque in. Temporibus nostrum doloribus quis et et aut iste asperiores. Voluptatem eligendi ut reprehenderit ut. Repellat amet accusamus in laborum deserunt consectetur ullam. Nostrum et illo non cupiditate. Cumque aut ratione impedit rerum inventore voluptas. Omnis quia fuga numquam reiciendis eligendi et. Cum sequi consequatur voluptatem earum labore. Consectetur quae rerum ipsa qui. Consequatur in aut molestiae officia labore. Sint voluptate tempora consequatur. Explicabo porro repudiandae sapiente optio. Nulla omnis quisquam eum quasi nemo. Eos voluptatem itaque et voluptatum voluptatem. Enim amet quo dignissimos itaque nihil et iure pariatur. Maxime molestiae est nobis reiciendis facere aperiam possimus debitis. Eum sint culpa sunt odit ut. Sint dolorem eum sit enim quibusdam voluptas quidem. Similique adipisci et modi enim neque. Et et tempora perspiciatis voluptatem corrupti quia laborum temporibus. Sed sit at molestias consequuntur mollitia. Aut eaque mollitia rerum omnis est voluptatibus corporis. Dolorem cumque ducimus saepe nihil laboriosam. Voluptatem dolore repudiandae voluptatum eius dolor velit impedit voluptatem. Molestiae est quibusdam tempore. Distinctio placeat dolorem modi amet. Autem expedita velit voluptates asperiores. Quas hic placeat fugiat vel. Quisquam aut optio et atque commodi. Quia eveniet non in qui voluptas. Esse voluptatem sed nihil quisquam maxime ut blanditiis. Veritatis nostrum eos repellat. Sint sed sunt ex placeat nostrum nisi. Est voluptatem natus itaque est. Neque rerum modi placeat. Voluptatibus fugiat odio blanditiis reprehenderit sequi fugiat. Eaque tempore et maxime aut sed. Occaecati vel et corporis laborum. Iure consectetur est et aut architecto quibusdam veritatis. Numquam cumque dicta ut deserunt perspiciatis at odio. Vel dolorum odit facere vitae magni ipsum. Omnis voluptas illo voluptas sed laborum aut itaque. Beatae sit tenetur inventore nobis molestiae quia eos. Et rem iure consequatur. Quia nemo ducimus hic veniam architecto. Culpa sit praesentium cupiditate veritatis aut ab odit quaerat. Itaque voluptates debitis saepe quisquam sunt. Sed et fugiat tempore inventore. Placeat sapiente temporibus magnam est. Temporibus enim ipsum est saepe dolor. Non ut consequatur aliquam fugiat consectetur voluptatem. Eligendi praesentium expedita voluptates cum aperiam iusto. Animi ea aperiam nobis dolores neque. Voluptatem quaerat perferendis doloremque error perspiciatis voluptas saepe. Consequatur praesentium saepe earum. Eligendi impedit quo et officia et pariatur quia. Excepturi eos vel inventore et et sunt. Cupiditate ut sequi tempora dolorem sunt. Qui consequatur eum dolorem voluptatum. Voluptatem ea vero fugiat dolor inventore eaque et deserunt. Quia dolorum voluptate doloribus qui est voluptatibus optio. Eaque accusantium nihil dolor et saepe. Iure suscipit magnam cum ad ut voluptatibus neque.', 11),
(18, '2025-02-13 00:47:38', '2025-02-13 00:47:38', 'Olin Harber', 30, 'Sed et aliquid et quis. Sint ut quibusdam illo voluptate deserunt delectus harum. Temporibus est aut deleniti adipisci sapiente. Hic quos quam illo quisquam minus quaerat accusamus. Fugiat dolor optio omnis saepe sed. Reprehenderit error dolor ea fugit tenetur. Maiores est quibusdam rerum rem perferendis et. Tenetur sunt qui qui necessitatibus dolorum dolores omnis. Distinctio sit hic quidem mollitia commodi. Maxime est sit et excepturi. Qui similique iure placeat repellendus qui qui rerum quibusdam. Delectus molestiae sequi nihil in qui. Nesciunt hic molestiae aut aut ipsa non. Beatae inventore ullam ullam repellat. Est et aut quia. Voluptatem ut est quam debitis. Quidem rem est reiciendis molestiae et maxime. Officia atque aliquid aut nemo. Numquam sunt sapiente accusamus sint impedit quos accusamus. Est sequi minima facere a aut eum amet. Sed molestias est doloremque. Ea ut labore alias qui labore et. Qui voluptates id est itaque. Ut ipsum natus quo eum enim beatae. Voluptatum adipisci quae consequatur beatae ut asperiores tenetur. Consequatur vitae cum et perferendis tempore occaecati ut. Dolor ut ea molestiae. At ut voluptatum est nihil. Reprehenderit ipsa quam nobis incidunt quia similique. Quas tempora assumenda exercitationem dignissimos sit optio maxime ut. Earum ab quo voluptate et ducimus. Velit et sed modi eligendi quia quis dolores. Ut et officia consequuntur delectus enim sequi laboriosam. Explicabo optio tenetur voluptatem minus molestias. Ut itaque in mollitia et sapiente ea nesciunt. Nihil pariatur quasi pariatur in rerum. Expedita eveniet praesentium id enim voluptatem aut quia. Omnis laudantium eum libero corrupti nesciunt quisquam. Explicabo voluptatem modi ut reprehenderit autem quasi. Voluptatem voluptatem temporibus ipsa tempora in iure tempora. Aliquid corrupti reiciendis earum perspiciatis est dicta. Id impedit provident quam. Incidunt cumque aut modi corrupti molestias natus. Doloribus non perspiciatis perspiciatis expedita quia laudantium. Facere ratione asperiores vel non doloremque dolor. Dolor voluptatem repudiandae error reiciendis animi. Ullam aut aliquid sequi aut doloribus consequuntur nostrum. Illo itaque sequi eum nam aut. Cupiditate et velit accusamus est ut repellat. Facilis deserunt voluptatem aspernatur dicta non aspernatur. Ab rem adipisci tempore ex. Omnis sit harum quisquam voluptas dignissimos. Dignissimos beatae dolor asperiores molestiae asperiores quis. At qui in dolor. Labore est velit rerum alias qui. Maxime repellendus ut dolore maxime quo. Laudantium ducimus enim neque dolor aut. Et ut in vel quis modi maiores explicabo. Quia sunt cupiditate quos incidunt voluptate. Voluptates rerum necessitatibus voluptate aut eligendi. Culpa cumque et expedita illo. Qui quisquam id quod illum.', 12),
(19, '2025-02-13 00:47:38', '2025-02-13 00:47:38', 'Earnestine Larkin', 51, 'Temporibus laudantium autem debitis natus. Quis ipsa quia et commodi. Eos aut perspiciatis quia et. Consequatur voluptate tempore harum magnam quo. Error doloribus accusamus omnis illum. Rerum reiciendis dicta provident. Dolores ab aliquam quidem quidem velit iusto. Dolores soluta quis cum. Ut velit qui qui incidunt quod. Iure aut magni sit placeat. Consequatur officiis quasi qui eos. Libero numquam ducimus voluptatem temporibus mollitia vero beatae sit. Architecto aut et quod at veritatis. Omnis enim distinctio reiciendis accusantium. Enim maxime iusto commodi commodi at deleniti laborum. Aut dolorem et beatae atque temporibus est rerum. Ea fugiat quia consequatur. Odit quod cupiditate aut nam laborum. Ratione aspernatur quo rerum harum aperiam ducimus. Voluptatibus blanditiis cumque in asperiores odit animi. In eligendi aspernatur voluptas autem enim. Officia eveniet voluptas impedit et accusantium ducimus. Nihil ut et id illo distinctio corrupti quasi. Dolorem sequi ut laborum repellat recusandae et ut earum. Nesciunt unde culpa eum eum ut laboriosam voluptates. Soluta aliquid autem reprehenderit fuga repellendus praesentium fuga. Odit delectus a sit quia accusantium rerum voluptate. Nobis quos facilis maiores nostrum ipsa ab ea. Temporibus fuga ipsam provident velit. Aut quod quasi corrupti accusantium veniam animi. Aut non totam commodi quia. Distinctio et sint qui perferendis. Voluptatum molestias vitae maiores fugit et autem. Vel dolor sint nostrum. Nihil hic laudantium et cumque earum minus. Odio enim aperiam tempore facere. Nulla soluta libero saepe sunt qui quidem. Quisquam vitae qui omnis quia. Omnis aliquam impedit et aut tempore ullam consequatur laudantium. Dolore quo corrupti nihil fuga ipsum ut. Tempore excepturi eos qui sed natus et unde. Modi a dolor est. Alias suscipit dolor enim minima facilis corporis sed. Occaecati quia reprehenderit nihil voluptates. Enim et dolores saepe sunt. Labore odit earum voluptatibus reiciendis quas. Enim sunt cumque dolores qui. Aut quo veritatis laudantium. Ipsa ratione autem cupiditate facere harum distinctio delectus cumque. Fuga veritatis dignissimos similique a fugiat velit quia. Earum tempore et quia consectetur sunt. Sint repellendus in voluptas omnis eum. Et temporibus vel molestias. Qui et deleniti tempora voluptatibus. Quis adipisci commodi accusamus nobis est dolorum est. Sunt libero ut nesciunt id enim nihil. Perspiciatis culpa tempore nihil rerum repellat eaque. Maxime non asperiores numquam numquam ut. Rerum eos nesciunt non eius quo repellat dolorem aliquid. Est reiciendis ut nesciunt quis. Est aliquam exercitationem in porro tempora eos. Fugiat quos pariatur illo qui. Labore ipsam est tempora dolore. Iusto omnis modi minus qui dolores quaerat.', 11),
(20, '2025-02-13 00:47:38', '2025-02-13 00:47:38', 'Alison Schumm', 48, 'Dolore ipsum error possimus esse voluptatem quam. At eveniet corrupti cum aspernatur et. At est fugiat ut cum quia. Qui dignissimos necessitatibus sit voluptates facilis. Voluptatem cupiditate adipisci vel voluptas pariatur. Ut iusto et maiores. Ut eius quam error nobis quidem eius. Consectetur velit numquam corporis dicta assumenda autem perferendis. Ipsa sed enim dolores et laborum. Doloremque vel quia reiciendis illo id. Similique est libero vero rem. Ut magnam eius eos et sapiente necessitatibus. Minima rem occaecati quis eos. Quasi laudantium vitae sed rem maxime enim. Placeat porro earum adipisci omnis harum nulla. Nulla pariatur amet ipsum pariatur et eum sunt. Vel provident culpa ut sunt sint. Natus dolor a id. Et numquam qui quia id. Voluptatum debitis voluptatem et et beatae. Et nobis sed iusto in sunt ad ea. Repellendus vitae rem laborum voluptatem aut soluta. Harum sit sed dolorem. Expedita error alias voluptatibus sit. Voluptate esse dolor placeat modi. Velit error incidunt et quod qui rerum nihil. Qui impedit enim vel ab fugit quia quidem. Corrupti quos ducimus ut possimus deserunt perferendis rem. Est dolore sit et consequatur saepe possimus. Maxime voluptas ullam ut et. Placeat adipisci perspiciatis aspernatur. Tempora qui nihil vitae. Aut tenetur temporibus tempora libero. Optio et modi aperiam et voluptatibus qui. Necessitatibus rerum ad cupiditate cumque. Porro aut voluptatem occaecati provident dolores. Cupiditate quibusdam eos dolorum. Rerum quisquam eos doloremque quo et. Accusantium mollitia consequatur assumenda eius. Ducimus sint deleniti possimus et repellat. Numquam ipsam sunt ullam enim illum impedit veritatis nemo. Omnis qui dolorem similique fugiat autem vitae aut. Quam minus temporibus aut incidunt. Nihil ut aut enim ut magni dolores. Illum consectetur repellat vel ut distinctio. Ipsa reprehenderit fuga cumque quod blanditiis ab quibusdam. Ut nulla eum magnam voluptatibus quis. Molestiae corporis laboriosam earum voluptatem placeat. Quidem nisi aliquam eos eum corrupti velit est. Commodi quis cum omnis iusto repudiandae quia. Blanditiis optio doloremque dolores praesentium. Repudiandae debitis totam quia minima. Maxime dignissimos nesciunt consequuntur reiciendis unde. Id quo alias ut architecto. Aut voluptatibus omnis eum a quia iste. Et odio harum est voluptatibus cum aut doloribus ut. Sit laboriosam accusamus hic error. Pariatur aut distinctio similique aliquam qui dolore. Velit magni sunt ut eius id. Laboriosam similique ratione sapiente placeat nostrum harum et. Aliquam corporis ratione adipisci ut quaerat in. Minima occaecati doloremque dolorem ut rerum quibusdam sed. Exercitationem officiis earum eum quisquam. Maxime voluptatum vero rerum alias consectetur qui voluptates. Consectetur reprehenderit consequuntur impedit cum. Quo possimus et laudantium corrupti totam. Vero inventore voluptatem sapiente distinctio voluptatum explicabo quis. Veniam cum et voluptas iusto. Ipsa sit occaecati repellat impedit nemo aliquam eveniet et. Fuga id quia ut. Delectus molestias aut ut aspernatur molestias maxime natus. Facilis omnis ut officiis doloremque nihil optio. Reiciendis sed aliquam amet. Molestiae voluptas quae possimus eos omnis ipsa ipsum. Nam corrupti dicta a et. Aut minus aut consequatur quia maiores et. Et natus veniam quia temporibus ut dignissimos. Fugiat voluptatem dolorem qui quis. Omnis esse et veritatis saepe voluptates saepe totam. Aut nesciunt sint aliquid porro earum. In nesciunt enim recusandae numquam et. Quis voluptas quia ipsa sed quo voluptatem. Repudiandae alias omnis eligendi laborum minima esse architecto vel. Ut voluptatem omnis qui rerum est ex autem. Harum magnam est quam distinctio eaque. Unde rerum cumque ut eligendi. Modi tempore cumque voluptas ad deleniti ut. Et a blanditiis cumque quod non animi et dolor. Molestiae quibusdam nesciunt qui omnis odio voluptatibus omnis. Quaerat vel repudiandae voluptates nobis vitae. Dicta non debitis et modi rerum atque consectetur. Neque eaque nihil ea qui magnam. Ea sint veniam quia in. Itaque officia pariatur ex hic officiis. Nostrum a qui voluptatem corporis optio. Magni rem autem accusamus maiores qui cupiditate. Voluptatem enim repellendus veniam autem adipisci aut aut. Commodi enim provident doloremque aut atque nulla.', 9),
(21, '2025-02-13 00:47:38', '2025-02-13 00:47:38', 'Ofelia Kertzmann', 49, 'Atque illum ut odit molestiae inventore. Iure odio officia et iusto. Voluptatibus ut consectetur placeat voluptates voluptate ut corporis ipsa. Et ea vitae officia totam est in. Ea provident qui consequuntur ipsa aut. Expedita quis et facilis autem ipsa magni. Doloribus deleniti eos qui minus veritatis. Ducimus voluptates repellat qui eos quae reiciendis veniam. Et molestiae aut perferendis enim eius. Animi et consequatur est eos ut non. Et eos in veritatis eum. Aut dicta ducimus velit atque est. Molestiae ea repellat ut aut et. Itaque ea molestiae veritatis maiores et aut voluptatibus. Sequi et nisi et mollitia voluptatem suscipit. Est reiciendis exercitationem facilis. Mollitia et sequi quaerat voluptas illo sit. Sit id odio autem adipisci ut. Neque atque facilis nesciunt est eos unde sint. Quos assumenda facere aut id magni nulla et iure. Iure qui et nihil dolore. Est adipisci quasi molestiae nam quas. Voluptate culpa autem tempora officiis mollitia voluptas rerum dolorum. Reiciendis ab rem nostrum temporibus adipisci aperiam sit. Expedita quasi fuga maxime sint. Voluptatem et atque omnis non aut. Magni est rerum est praesentium consequatur soluta ipsa. Consequuntur tempore itaque dolores nam repellendus. Unde dolor nulla omnis eos. Molestias rerum eaque quaerat soluta numquam quis iste. Mollitia accusantium blanditiis eos amet labore et. Numquam voluptate ipsa ipsa. Quae culpa voluptatem beatae veniam illum. Excepturi voluptatem animi odio repellat. Officia fugiat perspiciatis dolorem voluptas dolores blanditiis excepturi. Eum aut officiis velit et libero magnam autem. Occaecati autem id perferendis molestiae expedita. Quibusdam omnis harum dolores consequatur et rerum eos voluptates. Eaque quis occaecati autem incidunt et. Laborum impedit magni facilis eaque eos sed sint. Aut consequuntur adipisci veniam unde rerum corrupti velit. Amet illum voluptatem aliquam eaque eligendi sit. Hic modi rerum eveniet distinctio exercitationem. Nulla consequatur facilis magni error. Beatae nihil ut vel quasi soluta ut. Fugiat et nostrum blanditiis occaecati blanditiis cupiditate. Iusto porro quisquam maiores tempore ut aperiam sapiente. Quis et atque iusto mollitia eius ab facilis. Omnis adipisci incidunt libero quo minima. Quasi vel ut consequatur provident fugiat. Minima dolorum architecto consequuntur aperiam ut et. Quia molestiae perspiciatis est et quasi. Distinctio quidem est eum assumenda. Fuga esse eius ratione quis rerum. Aliquam corporis laudantium commodi nihil natus. Quidem sed rerum animi vel ut velit. Aut autem aliquam ad. Corrupti voluptates error in cum. Tempore vero non provident maiores et hic voluptas dolorem. Quia amet alias blanditiis maxime autem sequi dolor. Eaque et officiis omnis molestiae sed. Necessitatibus accusamus et officia minima dolore odit hic hic. Sapiente hic aut fugiat dolorem dolorem sit. Blanditiis ut repellendus id quia. Laborum voluptatem voluptatibus nobis id laboriosam ipsam explicabo repellendus. Sed aut voluptatibus illo ad et tempora. Nostrum architecto qui sed ad. Tempore et rerum aspernatur quis sed voluptates. Sit ut dolor sunt voluptatem dicta expedita vel. Excepturi atque natus ea perferendis odit non. Adipisci sed adipisci voluptatem dolores tempore nostrum necessitatibus. Libero quas est officia. Voluptatum dolorem non voluptatum magni beatae et animi. Impedit alias veniam sit. Tenetur molestias excepturi neque quasi dolorem. Sed ratione modi vel facere. Nobis velit numquam sed soluta. Enim nesciunt iste ullam et molestiae. Natus omnis eveniet non repellat consectetur. Provident neque repellendus voluptatem sed est et dicta. Expedita sit deleniti et delectus aut error consequatur. Consectetur eum ad voluptatem quis. Aut nulla beatae sit omnis. Porro tempora est molestiae in quaerat quae. Vel aspernatur est ex pariatur voluptas. Magni explicabo fugit et quos. Error error suscipit officiis dolorem iure dolores possimus. Et modi corporis unde tempora vel. Vero voluptas accusamus fugit consequatur et consequatur. Sit asperiores laborum commodi magnam quo asperiores ipsa. Iusto dolores mollitia voluptates nostrum voluptatem in.', 3),
(22, '2025-02-13 00:47:38', '2025-02-13 00:47:38', 'Kristina Yundt', 28, 'Laborum quaerat delectus enim harum eaque alias qui. Vitae quibusdam suscipit voluptatem id sapiente numquam. Sapiente quisquam nam accusantium voluptatem laboriosam voluptatem dolorem. Repellat voluptas voluptatem nobis in. Ut et eligendi blanditiis soluta aspernatur. Quibusdam molestias deserunt commodi. Est illum incidunt minima. Ducimus officiis beatae quis. Quibusdam sapiente quod velit sapiente. Ut distinctio facere eos et et dicta. Et non qui vel facere et. Voluptatem quae consequuntur itaque numquam. Aspernatur occaecati non voluptatem iste delectus. Est quibusdam distinctio quasi corrupti quam incidunt quidem. Dolor atque iusto atque quasi et. Voluptas eos magni eaque eveniet velit. Et eum enim qui rerum adipisci in. Eos illum voluptas quos facere. Omnis possimus et tempore repellendus qui quia suscipit. Omnis accusamus commodi deleniti fugiat fugit. Quia animi nemo dolores velit sed. Iure dolores tempora eum quidem nam dolorem in. Voluptatum impedit illo sint. Ullam aut beatae esse perferendis molestiae. Autem consequatur aut aliquid enim dolorem. Et adipisci sed praesentium illum consectetur vitae facilis. Quasi minima earum rerum optio. Velit ut inventore beatae quaerat tempora dolorum ipsum. Ut aut est repellendus asperiores exercitationem aperiam. Vel cupiditate harum reiciendis qui ut rerum autem. Earum veniam quia aspernatur sunt. A dolorem alias facilis nostrum voluptatem. Aut ea ab facere neque suscipit odit quis quam. Quia aut dolorem ea recusandae sed quae consequatur. Velit reprehenderit corrupti delectus minima sequi. Facere ipsa sit mollitia eos eum aut libero. Laboriosam alias eius eveniet. Et architecto ut voluptatem nostrum enim laborum. Qui nemo nesciunt unde necessitatibus. Sunt quam cumque non at dolores ad suscipit. Vel quis sint architecto vel. Et enim nesciunt porro dolorum repellat. Hic ut esse et omnis sint. Sed ipsa quis dolores ab eos praesentium. Explicabo eos reiciendis sit deleniti facilis. Soluta sed quibusdam esse nemo nihil veniam doloremque. Ea neque libero numquam iste. Sed ipsam omnis ipsum ad. Molestiae consectetur enim molestiae sequi suscipit. Tempore est facere beatae non repellat. Sit excepturi fugiat autem voluptas. Nulla a sed atque placeat nisi aut iure. Inventore dolorem voluptate saepe cupiditate enim. Voluptatem fugiat aut et sint eos. Et esse temporibus sint sed architecto. Ullam ab sapiente aut. Dicta repellat quam numquam dolor. Nostrum optio necessitatibus dignissimos optio voluptatem eaque. Aperiam placeat quia in dolores illo. Rerum beatae autem minus explicabo adipisci eveniet. Recusandae ullam culpa consequuntur qui et perferendis odit fugit. Et ex est fuga. Suscipit blanditiis dignissimos mollitia deserunt cum. Et eius non aliquam provident qui consectetur natus quas. Ea saepe maiores qui culpa. Voluptatem accusamus at sit sequi aut sit labore magni. Eos ea dolorem a id occaecati. Quod quibusdam consequatur qui distinctio adipisci tempore dolorum ullam. Placeat nobis vero aut laudantium ex et facere consectetur. Quo nisi dicta qui nemo mollitia. Ea quo ipsam qui inventore autem. Vel non aliquid blanditiis blanditiis inventore quas. Voluptas dolorum culpa officiis repellendus nam aliquam a. Beatae quo sint et. Voluptatem debitis aperiam inventore praesentium. Autem rerum eaque nam sit qui expedita sunt. Neque optio vitae similique accusamus. Ut dolorem ad eaque laudantium ullam sapiente eum. Sint nihil repellendus qui quos sit qui. Eius minima rerum laborum illo. Eos in nihil officia et quos veniam officiis. Saepe et quae totam perferendis aliquam laboriosam. Ut modi vel temporibus voluptas et hic cumque rerum. Temporibus fuga eos veniam dolores harum est. Velit magnam dolorem quisquam sapiente sed et. Explicabo dicta totam enim maiores ipsum qui. In molestias itaque culpa cum ut vitae. Unde voluptas qui est dolorem aut tempora nulla quia. Necessitatibus quod tempora in perspiciatis excepturi rem. Consequatur voluptates sed dolorem est magni. Ut cum reprehenderit ut est repellendus non. Et et maiores asperiores labore rem. Quam velit porro accusamus cum. Consequuntur ullam est mollitia excepturi ipsa. Similique libero cum consequatur mollitia ea. Quaerat eos nostrum omnis totam natus quasi. Voluptatem incidunt in ad inventore aut. Unde quam nisi voluptatibus reiciendis. Optio ea molestias voluptas ratione. Eum cumque praesentium pariatur voluptas dignissimos ut debitis. Quasi dolorem expedita quas. Minima voluptatem sed ea id est quam sit perferendis.', 8),
(23, '2025-02-13 00:47:38', '2025-02-13 00:47:38', 'Abner Wisoky', 23, 'Quaerat id rerum in incidunt. Dolor doloremque quam tenetur vero dolore quis. Eligendi ducimus sapiente sapiente dolorum quos magni. Quis pariatur aut accusantium doloremque ab at repellat. Ut similique repudiandae sunt vitae labore sed qui. Nemo assumenda voluptas corporis velit iure dolorem. Ea distinctio ut beatae rerum. Blanditiis accusantium aut sit minima culpa excepturi est. Officiis eveniet rem sit esse est. In est dolores voluptate eligendi soluta illo numquam. Eum sit repellat accusantium. Qui excepturi a nisi neque in. Enim culpa dolor sed et eaque molestiae et velit. Aut ut ut nesciunt et tempore et nobis. Deserunt fugiat aut illum doloremque at culpa accusamus qui. Ut rem qui distinctio sed eum. Ut exercitationem voluptatem excepturi. Nemo doloremque ipsum sequi expedita voluptatem sed. Eligendi incidunt quo excepturi ad nemo distinctio quas. Nesciunt recusandae praesentium vel exercitationem quam. Fugiat consectetur ipsum aut dolorum. Soluta qui ipsa accusantium. Molestiae harum harum cum repudiandae. Eveniet est eaque aut natus natus ipsum. Omnis et eius velit ducimus atque temporibus. Ut labore quia id velit. Molestias dolores pariatur est expedita est et ex. Veniam qui eum voluptas. Corrupti consequatur voluptatem in molestiae magnam. Rerum dolores sed molestiae ab nemo doloremque. Delectus odit iusto expedita a in voluptatibus vitae. Id qui aut id at saepe ea nemo assumenda. Temporibus ut labore sed inventore sint voluptatum unde. Nihil perferendis ea recusandae qui nobis quibusdam. Ipsum voluptas odit non aspernatur aut odio. Sint quasi deleniti voluptatem quia minus. Magni repellendus voluptatem et sit enim. Nemo rerum excepturi vel officiis ea ab deserunt. Recusandae provident nobis mollitia. Reprehenderit ipsum unde iure natus consectetur minima necessitatibus. Consequatur id voluptatem velit nobis eligendi illum. Nostrum quis et incidunt aut. Ut expedita veritatis omnis laborum. Illo impedit sed aut nihil architecto quis. Facere dignissimos dolorum vel perferendis provident perspiciatis dicta. Molestiae mollitia exercitationem aut praesentium. Ipsum enim perferendis harum aut perferendis. Placeat aspernatur laboriosam non quis nihil possimus. Molestiae soluta voluptatibus et iure eum incidunt nulla. Maiores veniam neque veritatis ut quia. Dolore quia iste ut blanditiis blanditiis vel omnis. Et in optio et adipisci aliquam quibusdam sint. Culpa earum facilis sed in dignissimos temporibus commodi. Pariatur facere ipsum eum minima. Aut et adipisci quos sit itaque a. Voluptas et eum excepturi ipsa delectus non. Ut et praesentium nobis officiis. Delectus in dolores ut quod minus. Laudantium cum voluptas et et et est eum. Error non sapiente adipisci ea est eos ratione. Beatae natus est ea ut. Fugit voluptates consequatur earum. Nemo nulla vel distinctio non cum. Pariatur nihil ipsum ducimus voluptas. Assumenda quis sed eum fugiat. Ea sed saepe et veniam deleniti fuga. Commodi maxime quo dolorem ratione et ipsam laborum. Cupiditate culpa id sed dolor labore id. Dignissimos velit odio illum. Rerum est et nam et. Quis velit quas velit. Aliquid id occaecati optio aut est. Consequuntur id enim labore ut consequatur reiciendis quo. Debitis voluptatem sit dolorum voluptatem aut tempore eius voluptates. Saepe quis voluptatum tenetur dolor. Non quae dolor quia molestiae repudiandae iusto dolorem. Dicta fugiat est aut perferendis eum aut soluta soluta. Et quo ex in voluptatem rerum. Aut neque nobis et excepturi voluptatem. Voluptate esse velit cumque id magnam. Inventore ea officiis numquam officia iusto nulla. Nesciunt et ut occaecati inventore unde. Porro accusamus veritatis doloremque a exercitationem harum. Voluptates similique tempore officia saepe non non quibusdam. Aut facere delectus modi ab molestias. Consequatur eaque et ad autem aliquam molestiae. Aliquam et delectus eos. Voluptatum necessitatibus sed atque. Ea aut repellat asperiores dignissimos repellat aperiam. Qui sint necessitatibus doloribus et. Placeat totam est rem labore ad magni placeat. Dignissimos qui dignissimos nam et et expedita totam. Consequuntur et animi voluptates et minima enim temporibus. Enim enim consequuntur odio magnam aspernatur sint. Aut qui harum accusamus tempore repellendus voluptate velit. Ex vitae similique ut maxime totam culpa autem.', 10),
(24, '2025-02-13 00:47:38', '2025-02-13 00:47:38', 'Hope Metz', 53, 'Rerum nam nostrum accusamus incidunt impedit ipsa aliquam. Voluptatem asperiores aut at ut eveniet dignissimos. Ab laborum ex impedit totam sunt. Mollitia exercitationem ipsum enim qui illo. Sit fuga culpa facere. Asperiores et voluptatem quaerat ut est ex unde tenetur. Illum quia labore repellat esse praesentium. Ex non rem nihil nulla quidem. Possimus labore vel illo. Veniam facilis assumenda voluptatum corporis ut ut quia. Atque sapiente quis quidem architecto aperiam. Ab enim odio dicta aut qui molestiae repudiandae. Sint iure delectus sed saepe. Nam porro quia ipsam eos. Nulla eligendi assumenda sunt sed. In distinctio voluptas animi incidunt ut sint. Nesciunt nostrum assumenda qui sequi eum sunt. Voluptatibus perspiciatis atque et vel. Quod tempore voluptas sed expedita aperiam consectetur. Quidem ullam enim eos. Quia odio sed sint tenetur. Officiis fuga aut aspernatur consequuntur itaque blanditiis esse. Sunt repellat accusamus rerum qui cupiditate. Id sunt distinctio autem. Esse nulla et quisquam molestiae. Et non voluptatum reprehenderit cum ratione corporis amet. Odit quae labore ut distinctio aut est. Omnis eius molestiae molestiae dolorem quae. Et velit esse saepe. Veritatis officiis quibusdam explicabo ut. Nulla ipsum vitae ad molestiae est. Corrupti eligendi consectetur vel quaerat dolores omnis non est. Distinctio quaerat et et. Quos totam repudiandae molestiae et eius. Nobis est totam quod illo quae aut architecto. Veniam nam quia quas quibusdam voluptatibus natus. Non labore neque rerum harum. Dolorum quae cum nesciunt rerum. Suscipit quidem eos natus esse. Error praesentium eius explicabo est officia iste. Non ratione saepe veniam cupiditate quam voluptatem at. Perspiciatis autem atque est ratione. Consectetur rerum temporibus temporibus aut. Ullam iusto id est totam quis et voluptatem. Omnis qui est consequatur minima error qui sequi. Fugit id architecto molestiae unde provident illum. At iste odio sequi rerum optio. Et reiciendis cum eligendi nostrum nobis atque. Voluptatem voluptate esse ad tempora aut. Doloribus soluta blanditiis non nostrum facere in dicta aut. Officiis nulla voluptas voluptate beatae nulla. Omnis harum nulla voluptas debitis sed ullam aut consequatur. Numquam fugiat quia rerum quos deserunt quas. Autem qui non eius veniam rerum. Ut voluptatem cumque perferendis ut reprehenderit. Sunt omnis mollitia quisquam repellendus. Aspernatur id provident excepturi voluptatem enim soluta. Sed eius velit quisquam hic reprehenderit est. Eos hic voluptatem neque optio officia temporibus. Maiores ab velit omnis placeat vitae. Aut et dolores delectus et tempore et culpa explicabo. Cumque atque eligendi adipisci sit exercitationem itaque quam. Aut quidem aut officia et sunt animi. Minima fugit numquam et ipsum perspiciatis. Sit at eveniet hic ab autem enim dolores. Incidunt est voluptates delectus iure praesentium autem. Aut eos exercitationem ut voluptatem quia. Commodi quia iusto unde doloribus quis. Illum inventore reiciendis quis dolor accusamus facilis. Laboriosam et iure et. Fugit officiis facilis esse occaecati assumenda sit suscipit. Nam et aut sed omnis inventore rerum. Minima reiciendis recusandae esse accusantium blanditiis. Sed sit animi laudantium illo magnam officiis iste. Odit et non modi eos sunt. Et debitis aperiam vel recusandae voluptatum incidunt atque veritatis. Blanditiis est nostrum distinctio. Dignissimos architecto nesciunt ipsa vel tempore voluptas id. Dolores quod corporis exercitationem ut adipisci quam ut sint. Aut et autem id. In odit aut consequatur maiores corporis ducimus rem. Doloribus est velit possimus. In assumenda quisquam debitis rem adipisci voluptatem repellendus. Labore qui ut quaerat autem nam. Nam eos quod porro voluptatibus ducimus temporibus quis enim. Itaque repellat assumenda voluptas. Itaque est aut iusto ea natus est. Et qui nulla autem laboriosam laboriosam nemo. Et ut autem animi omnis nobis nulla minima sed. In et consequatur et aut ipsam sint vel. Hic quia cum pariatur quo. Fugiat minus modi eveniet expedita natus quis ut. Quia laboriosam est facere provident sint rerum. Sint voluptatem voluptatem vel. Non fugiat sint nemo alias. Unde officiis iure est harum qui sit. Corporis ut aut error illo reprehenderit fugiat quia voluptatem. Qui sunt quam hic error vero omnis omnis neque. In aut quo aut a et ad dolore quisquam. Rerum sit corrupti nostrum ex. Delectus occaecati similique voluptatem omnis cumque. Ut molestias voluptas aut libero et. Aut quis quia molestiae in doloremque nihil. Facilis officiis molestiae magni nihil harum ea earum. Magni dolorem vel tenetur sunt quia. Aliquam est dolor natus a consequatur ex amet. Et impedit rerum harum perferendis totam. Quidem ipsam omnis et in. Aspernatur quae vel ut facilis.', 6),
(25, '2025-02-13 00:47:38', '2025-02-13 00:47:38', 'Betsy Dare IV', 38, 'Occaecati dolorem non ex in. Omnis delectus consequatur dignissimos neque. Ullam qui est odio in. Et ad libero accusantium. Molestiae et deserunt molestiae corporis aperiam doloribus maiores voluptatum. Sit veritatis eveniet vitae. Dolor dolorem necessitatibus voluptas molestiae odit. Quo aut sit omnis sunt et qui. Asperiores voluptas consequatur non necessitatibus dolore ut nulla. Exercitationem tempore sed autem fuga aliquam. Dolore qui non atque reprehenderit. Ad nobis dolorem laboriosam voluptate ipsa ut ut. Consectetur rerum quo quod et quo. Voluptatibus qui culpa quibusdam voluptates. Totam saepe accusamus veritatis hic. Aut sunt voluptas quas quia harum eum aut. Voluptatem et quaerat vel ratione nobis. Maiores sit est sit. At sunt eos quisquam amet hic perferendis quas. Sapiente aspernatur suscipit consectetur consequatur fuga. Aut rem quasi culpa. Repellat fugit perferendis quam tenetur fuga. Molestiae dolores natus ratione ut. Nihil quo est et esse. Vitae laboriosam vitae tenetur et debitis. Omnis nesciunt velit reprehenderit nihil placeat corrupti voluptates. Ipsum ad nulla soluta dicta dolores at. Aperiam non incidunt nostrum voluptas voluptas. Veniam et voluptas aut. Officiis ullam voluptatem enim repellendus impedit. Nihil excepturi quaerat sequi error expedita nihil nihil. Et soluta possimus vitae molestias quia officiis. Et laboriosam aut et doloribus. Totam libero dignissimos ut esse pariatur natus. Aut quia corrupti accusantium necessitatibus. Nulla soluta quia consequuntur quia. Distinctio quia velit ut est. Quia omnis exercitationem velit omnis temporibus. Excepturi ducimus quia consequatur non earum esse tempore. Animi tempore qui quibusdam ex. Sint eos sed architecto ut aut assumenda asperiores. Rerum aut molestiae eum maxime. Et nobis dolor et nisi. Blanditiis eos sunt aut eius. Rem eos unde odio adipisci sint ipsa architecto. In dicta aliquid velit deserunt quia et. Et qui repellendus nobis sunt doloremque minima maxime. Et vero perspiciatis sunt nihil nemo est modi. Nam quisquam corporis illo optio molestiae hic. Et saepe blanditiis ex sed tempore cupiditate quas. Sed aliquam beatae facere sequi quo. Commodi sed dolor non fugiat excepturi culpa est. Sit sed qui consequatur a quas maxime. Suscipit voluptate blanditiis fuga quia ea. Ea autem quo accusamus et at corrupti et. Sequi voluptates error expedita est occaecati inventore quam tenetur. Eos esse eveniet facilis beatae nisi nemo. Voluptas fugit maiores minus et odit dolor ut delectus. Nihil sunt quibusdam omnis ullam hic ea. Repellendus ut et quis in. Quas fugit quisquam accusantium nisi numquam. Fuga similique ad dignissimos eos voluptatum ipsum facere. Consequatur quidem necessitatibus dolor tenetur enim voluptas error. Et fugit impedit voluptas minima et qui. Quas adipisci nihil et non non quia fugit rerum. Impedit quis doloribus nam suscipit dolorum nihil repellat nesciunt. Ut qui in dolorum deleniti. Earum ducimus neque et tempora voluptas.', 9),
(29, '2025-02-17 19:01:46', '2025-02-17 19:37:25', 'edit sample', 44, 'asdfasdfasdfasdasdasdfasdf', 5);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `cache`
--
ALTER TABLE `cache`
  ADD PRIMARY KEY (`key`);

--
-- Indexes for table `cache_locks`
--
ALTER TABLE `cache_locks`
  ADD PRIMARY KEY (`key`);

--
-- Indexes for table `migrations`
--
ALTER TABLE `migrations`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `offices`
--
ALTER TABLE `offices`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `offices_office_number_unique` (`office_number`);

--
-- Indexes for table `password_reset_tokens`
--
ALTER TABLE `password_reset_tokens`
  ADD PRIMARY KEY (`email`);

--
-- Indexes for table `sessions`
--
ALTER TABLE `sessions`
  ADD PRIMARY KEY (`id`),
  ADD KEY `sessions_user_id_index` (`user_id`),
  ADD KEY `sessions_last_activity_index` (`last_activity`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `users_email_unique` (`email`);

--
-- Indexes for table `workers`
--
ALTER TABLE `workers`
  ADD PRIMARY KEY (`id`),
  ADD KEY `workers_office_id_foreign` (`office_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `migrations`
--
ALTER TABLE `migrations`
  MODIFY `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT for table `offices`
--
ALTER TABLE `offices`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `workers`
--
ALTER TABLE `workers`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=30;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `workers`
--
ALTER TABLE `workers`
  ADD CONSTRAINT `workers_office_id_foreign` FOREIGN KEY (`office_id`) REFERENCES `offices` (`id`) ON DELETE CASCADE;
--
-- Database: `book_management`
--
CREATE DATABASE IF NOT EXISTS `book_management` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE `book_management`;

-- --------------------------------------------------------

--
-- Table structure for table `books`
--

CREATE TABLE `books` (
  `id` int(11) NOT NULL,
  `book` varchar(255) NOT NULL,
  `author` varchar(50) NOT NULL,
  `date` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `books`
--
ALTER TABLE `books`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `books`
--
ALTER TABLE `books`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;
--
-- Database: `demo_db`
--
CREATE DATABASE IF NOT EXISTS `demo_db` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE `demo_db`;

-- --------------------------------------------------------

--
-- Table structure for table `task`
--

CREATE TABLE `task` (
  `task_id` int(11) NOT NULL,
  `task_name` varchar(50) NOT NULL,
  `date` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `task`
--

INSERT INTO `task` (`task_id`, `task_name`, `date`) VALUES
(16, 'this is my first task', '2025-04-30'),
(17, 'this is my second task', '2025-04-30'),
(18, 'and this is third', '2025-04-30'),
(19, '4th', '2025-04-30');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `task`
--
ALTER TABLE `task`
  ADD PRIMARY KEY (`task_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `task`
--
ALTER TABLE `task`
  MODIFY `task_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;
--
-- Database: `employee`
--
CREATE DATABASE IF NOT EXISTS `employee` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE `employee`;

-- --------------------------------------------------------

--
-- Table structure for table `employees`
--

CREATE TABLE `employees` (
  `id` int(11) NOT NULL,
  `employee` varchar(100) NOT NULL,
  `date` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `employees`
--

INSERT INTO `employees` (`id`, `employee`, `date`) VALUES
(4, 'First employee', '2025-05-26'),
(5, 'dd', '2025-05-26');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `employees`
--
ALTER TABLE `employees`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `employees`
--
ALTER TABLE `employees`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;
--
-- Database: `job_portal_db`
--
CREATE DATABASE IF NOT EXISTS `job_portal_db` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE `job_portal_db`;

-- --------------------------------------------------------

--
-- Table structure for table `admin`
--

CREATE TABLE `admin` (
  `username` varchar(20) NOT NULL,
  `email` varchar(30) NOT NULL,
  `password` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `admin`
--

INSERT INTO `admin` (`username`, `email`, `password`) VALUES
('jem', 'jem@admin.com', '$2b$12$a20x8Hn1uiymEFVSrf.5zO4B3bZCWemh8WpuSVPKpbBVN.9RFkNUG');

-- --------------------------------------------------------

--
-- Table structure for table `applications`
--

CREATE TABLE `applications` (
  `application_id` bigint(20) UNSIGNED NOT NULL,
  `job_id` bigint(20) UNSIGNED NOT NULL,
  `seeker_id` bigint(20) UNSIGNED NOT NULL,
  `resume_url` varchar(255) NOT NULL,
  `cover_letter` text DEFAULT NULL,
  `status` enum('applied','reviewed','shortlisted','rejected') DEFAULT 'applied',
  `applied_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `applications`
--

INSERT INTO `applications` (`application_id`, `job_id`, `seeker_id`, `resume_url`, `cover_letter`, `status`, `applied_at`) VALUES
(123, 1, 139, 'none', 'none', 'applied', '2025-04-07 10:31:02');

-- --------------------------------------------------------

--
-- Table structure for table `availability`
--

CREATE TABLE `availability` (
  `availability_id` bigint(20) UNSIGNED NOT NULL,
  `employer_id` bigint(20) UNSIGNED NOT NULL,
  `job_id` bigint(20) UNSIGNED NOT NULL,
  `start_time` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `end_time` timestamp NULL DEFAULT NULL,
  `timezone` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `employers`
--

CREATE TABLE `employers` (
  `employer_id` bigint(20) UNSIGNED NOT NULL,
  `email` varchar(255) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `last_login` timestamp NULL DEFAULT NULL,
  `company_name` varchar(255) NOT NULL,
  `industry` varchar(100) DEFAULT NULL,
  `company_size` int(11) DEFAULT NULL CHECK (`company_size` > 0),
  `website` varchar(255) DEFAULT NULL,
  `logo_url` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `employers`
--

INSERT INTO `employers` (`employer_id`, `email`, `password_hash`, `created_at`, `last_login`, `company_name`, `industry`, `company_size`, `website`, `logo_url`) VALUES
(2, 'kamjijajajo@gmail.com', '$2b$12$EmVDH7PYPLQSpKkBqN4Mterb9N5buSsJN9WvGOAWjFkscfIsryAA.', '2025-03-21 09:01:05', NULL, 'Innovatech', 'Programming', 1, '', ''),
(3, 'kanjijajajo@gmail.com', '$2b$12$hpw1pAYj1C96f4gtXtuhb.N3B/kVTbbNZLK4/zSJjohueFsuHV4Xm', '2025-03-21 09:03:05', '2025-05-05 07:54:19', 'company001', 'Programming', 1, '', '');

-- --------------------------------------------------------

--
-- Table structure for table `interviews`
--

CREATE TABLE `interviews` (
  `interview_id` bigint(20) UNSIGNED NOT NULL,
  `availability_id` bigint(20) UNSIGNED NOT NULL,
  `seeker_id` bigint(20) UNSIGNED NOT NULL,
  `status` enum('scheduled','confirmed','completed','cancelled') DEFAULT 'scheduled'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `jobs`
--

CREATE TABLE `jobs` (
  `job_id` bigint(20) UNSIGNED NOT NULL,
  `employer_id` bigint(20) UNSIGNED NOT NULL,
  `title` varchar(255) NOT NULL,
  `description` text NOT NULL,
  `location` varchar(100) NOT NULL,
  `salary_range` varchar(50) DEFAULT NULL,
  `employment_type` enum('full_time','part_time','contract','internship') NOT NULL,
  `posted_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `expires_at` timestamp NULL DEFAULT NULL,
  `status` enum('active','paused','closed') DEFAULT 'active'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `jobs`
--

INSERT INTO `jobs` (`job_id`, `employer_id`, `title`, `description`, `location`, `salary_range`, `employment_type`, `posted_at`, `expires_at`, `status`) VALUES
(1, 3, 'progamming', 'a programming job', 'manila', '35,000 - 50,000', 'contract', '2025-03-23 03:18:19', '2025-04-22 16:00:00', 'active'),
(2, 3, 'progamming', 'a programming job 1', 'manila', '35,000 - 50,000', 'contract', '2025-03-23 03:18:19', '2025-04-22 16:00:00', 'closed'),
(3, 2, 'progamming', 'a programming job 1', 'manila', '35,000 - 50,000', 'contract', '2025-03-23 03:18:19', '2025-04-22 16:00:00', 'active');

-- --------------------------------------------------------

--
-- Table structure for table `job_alerts`
--

CREATE TABLE `job_alerts` (
  `alert_id` bigint(20) UNSIGNED NOT NULL,
  `seeker_id` bigint(20) UNSIGNED NOT NULL,
  `search_terms` varchar(255) DEFAULT NULL,
  `location` varchar(100) DEFAULT NULL,
  `frequency` enum('daily','weekly','instant') DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `job_interest`
--

CREATE TABLE `job_interest` (
  `interest_id` bigint(20) UNSIGNED NOT NULL,
  `user_id` bigint(20) UNSIGNED NOT NULL,
  `job_interest` varchar(255) NOT NULL,
  `job_type` enum('Full-time','Part-time','Freelance','Internship') NOT NULL,
  `preferred_location` varchar(255) NOT NULL,
  `expected_salary_range` varchar(100) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `job_interest`
--

INSERT INTO `job_interest` (`interest_id`, `user_id`, `job_interest`, `job_type`, `preferred_location`, `expected_salary_range`, `created_at`) VALUES
(10, 139, 'programming', 'Freelance', 'Hybrid', '20,000 - 35,000', '2025-04-16 02:01:28');

-- --------------------------------------------------------

--
-- Table structure for table `job_seekers`
--

CREATE TABLE `job_seekers` (
  `seeker_id` bigint(20) UNSIGNED NOT NULL,
  `email` varchar(255) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `last_login` timestamp NULL DEFAULT NULL,
  `first_name` varchar(100) NOT NULL,
  `last_name` varchar(100) NOT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `province` varchar(100) DEFAULT NULL,
  `municipality` varchar(100) DEFAULT NULL,
  `degree` varchar(100) DEFAULT NULL,
  `portfolio_url` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `job_seekers`
--

INSERT INTO `job_seekers` (`seeker_id`, `email`, `password_hash`, `created_at`, `last_login`, `first_name`, `last_name`, `phone`, `province`, `municipality`, `degree`, `portfolio_url`) VALUES
(139, 'jemcarlo46@gmail.com', '$2b$12$jJsAP1.XiA4IFyrGxSCW0eeHEPop1rxc2Gz8XnKcUjDkthM1iwjRC', '2025-03-25 02:49:13', '2025-05-04 05:42:15', 'Jemcarlo', 'Austria', '09207766194', 'Pangasinan', '', 'bsit', '');

-- --------------------------------------------------------

--
-- Table structure for table `job_skills`
--

CREATE TABLE `job_skills` (
  `job_id` bigint(20) UNSIGNED NOT NULL,
  `skill_id` bigint(20) UNSIGNED NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `job_submissions`
--

CREATE TABLE `job_submissions` (
  `id` int(11) NOT NULL,
  `recruiter_id` int(11) NOT NULL,
  `title` varchar(255) NOT NULL,
  `description` text NOT NULL,
  `type` enum('full-time','part-time','contract','freelance') NOT NULL,
  `status` enum('new','pending','approved','rejected') NOT NULL DEFAULT 'new',
  `location` varchar(255) DEFAULT NULL,
  `salary_range` varchar(100) DEFAULT NULL,
  `submission_date` datetime DEFAULT current_timestamp(),
  `applicant_count` int(11) DEFAULT 0,
  `approved_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `messages`
--

CREATE TABLE `messages` (
  `message_id` bigint(20) UNSIGNED NOT NULL,
  `sender_id` bigint(20) UNSIGNED NOT NULL,
  `conversation_id` varchar(50) NOT NULL,
  `sender_type` enum('employer','job_seeker') NOT NULL,
  `receiver_id` bigint(20) UNSIGNED NOT NULL,
  `receiver_type` enum('employer','job_seeker') NOT NULL,
  `content` text NOT NULL,
  `sent_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `is_read` tinyint(1) DEFAULT 0,
  `is_message_deleted` enum('false','true') NOT NULL,
  `is_conversation_deleted_by_sender` enum('false','true') NOT NULL,
  `is_conversation_deleted_by_receiver` enum('false','true') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `messages`
--

INSERT INTO `messages` (`message_id`, `sender_id`, `conversation_id`, `sender_type`, `receiver_id`, `receiver_type`, `content`, `sent_at`, `is_read`, `is_message_deleted`, `is_conversation_deleted_by_sender`, `is_conversation_deleted_by_receiver`) VALUES
(3, 139, '575067013220190', 'job_seeker', 3, 'employer', 'hello', '2025-05-05 02:06:30', 0, 'false', 'false', 'false'),
(4, 3, '575067013220190', 'employer', 139, 'employer', 'hey?', '2025-05-05 02:06:41', 0, 'false', 'false', 'false');

-- --------------------------------------------------------

--
-- Table structure for table `notifications`
--

CREATE TABLE `notifications` (
  `notification_id` bigint(20) UNSIGNED NOT NULL,
  `user_id` bigint(20) UNSIGNED NOT NULL,
  `user_type` enum('employer','job_seeker') NOT NULL,
  `message` text NOT NULL,
  `is_read` tinyint(1) DEFAULT 0,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `otp_codes`
--

CREATE TABLE `otp_codes` (
  `id` bigint(20) NOT NULL,
  `email` varchar(255) NOT NULL,
  `otp_code` varchar(6) NOT NULL,
  `expiry_time` datetime NOT NULL,
  `is_valid` tinyint(1) DEFAULT 1,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `otp_codes`
--

INSERT INTO `otp_codes` (`id`, `email`, `otp_code`, `expiry_time`, `is_valid`, `created_at`) VALUES
(1, 'jemcarlo46@gmail.com', '171150', '2025-03-19 09:09:29', 1, '2025-03-19 00:59:29');

-- --------------------------------------------------------

--
-- Table structure for table `password_reset_tokens`
--

CREATE TABLE `password_reset_tokens` (
  `id` int(11) NOT NULL,
  `email` varchar(255) NOT NULL,
  `token` varchar(255) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `expiry` timestamp NOT NULL DEFAULT current_timestamp(),
  `used` tinyint(1) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `qualifications`
--

CREATE TABLE `qualifications` (
  `qualification_id` bigint(20) UNSIGNED NOT NULL,
  `seeker_id` bigint(20) UNSIGNED NOT NULL,
  `degree` varchar(80) NOT NULL,
  `school_graduated` varchar(100) NOT NULL,
  `certifications` varchar(255) DEFAULT NULL,
  `specialized_training` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `qualifications`
--

INSERT INTO `qualifications` (`qualification_id`, `seeker_id`, `degree`, `school_graduated`, `certifications`, `specialized_training`) VALUES
(10, 139, 'asdasdasd', 'bcc', 'none', 'programming');

-- --------------------------------------------------------

--
-- Table structure for table `ratings`
--

CREATE TABLE `ratings` (
  `rating_id` bigint(20) UNSIGNED NOT NULL,
  `rater_id` bigint(20) UNSIGNED NOT NULL,
  `rater_type` enum('employer','job_seeker') NOT NULL,
  `ratee_id` bigint(20) UNSIGNED NOT NULL,
  `ratee_type` enum('employer','job_seeker') NOT NULL,
  `job_id` bigint(20) UNSIGNED NOT NULL,
  `score` tinyint(4) DEFAULT NULL CHECK (`score` between 1 and 5),
  `review` text DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `saved_jobs`
--

CREATE TABLE `saved_jobs` (
  `saved_job_id` bigint(20) UNSIGNED NOT NULL,
  `seeker_id` bigint(20) UNSIGNED NOT NULL,
  `job_id` bigint(20) UNSIGNED NOT NULL,
  `saved_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `seeker_profiles`
--

CREATE TABLE `seeker_profiles` (
  `id` int(11) NOT NULL,
  `user_id` bigint(20) UNSIGNED NOT NULL,
  `about` text DEFAULT NULL,
  `experience_title` varchar(255) DEFAULT NULL,
  `company` varchar(255) DEFAULT NULL,
  `experience_date` varchar(255) DEFAULT NULL,
  `experience_description` text DEFAULT NULL,
  `resume` varchar(255) DEFAULT NULL,
  `linkedin` varchar(255) DEFAULT NULL,
  `github` varchar(255) DEFAULT NULL,
  `twitter` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `seeker_skills`
--

CREATE TABLE `seeker_skills` (
  `seeker_id` bigint(20) UNSIGNED NOT NULL,
  `skill_id` bigint(20) UNSIGNED NOT NULL,
  `proficiency` enum('beginner','intermediate','expert') DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `skills`
--

CREATE TABLE `skills` (
  `skill_id` bigint(20) UNSIGNED NOT NULL,
  `name` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `verified_users`
--

CREATE TABLE `verified_users` (
  `email` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `verified_users`
--

INSERT INTO `verified_users` (`email`) VALUES
('jemcarlo46@gmail.com'),
('kanjijajajo@gmail.com');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `admin`
--
ALTER TABLE `admin`
  ADD UNIQUE KEY `email` (`email`);

--
-- Indexes for table `applications`
--
ALTER TABLE `applications`
  ADD PRIMARY KEY (`application_id`),
  ADD KEY `idx_job_id` (`job_id`),
  ADD KEY `idx_seeker_id` (`seeker_id`),
  ADD KEY `idx_status` (`status`);

--
-- Indexes for table `availability`
--
ALTER TABLE `availability`
  ADD PRIMARY KEY (`availability_id`),
  ADD KEY `idx_employer_id` (`employer_id`),
  ADD KEY `idx_job_id` (`job_id`);

--
-- Indexes for table `employers`
--
ALTER TABLE `employers`
  ADD PRIMARY KEY (`employer_id`),
  ADD UNIQUE KEY `email` (`email`),
  ADD KEY `idx_email` (`email`);

--
-- Indexes for table `interviews`
--
ALTER TABLE `interviews`
  ADD PRIMARY KEY (`interview_id`),
  ADD KEY `idx_availability_id` (`availability_id`),
  ADD KEY `idx_seeker_id` (`seeker_id`);

--
-- Indexes for table `jobs`
--
ALTER TABLE `jobs`
  ADD PRIMARY KEY (`job_id`),
  ADD KEY `idx_employer_id` (`employer_id`),
  ADD KEY `idx_status` (`status`);

--
-- Indexes for table `job_alerts`
--
ALTER TABLE `job_alerts`
  ADD PRIMARY KEY (`alert_id`),
  ADD KEY `idx_seeker_id` (`seeker_id`);

--
-- Indexes for table `job_interest`
--
ALTER TABLE `job_interest`
  ADD PRIMARY KEY (`interest_id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `job_seekers`
--
ALTER TABLE `job_seekers`
  ADD PRIMARY KEY (`seeker_id`),
  ADD UNIQUE KEY `email` (`email`),
  ADD UNIQUE KEY `phone` (`phone`),
  ADD KEY `idx_email` (`email`);

--
-- Indexes for table `job_skills`
--
ALTER TABLE `job_skills`
  ADD PRIMARY KEY (`job_id`,`skill_id`),
  ADD KEY `idx_job_id` (`job_id`),
  ADD KEY `idx_skill_id` (`skill_id`);

--
-- Indexes for table `job_submissions`
--
ALTER TABLE `job_submissions`
  ADD PRIMARY KEY (`id`),
  ADD KEY `recruiter_id` (`recruiter_id`);

--
-- Indexes for table `messages`
--
ALTER TABLE `messages`
  ADD PRIMARY KEY (`message_id`),
  ADD KEY `idx_sender_id` (`sender_id`),
  ADD KEY `idx_receiver_id` (`receiver_id`);

--
-- Indexes for table `notifications`
--
ALTER TABLE `notifications`
  ADD PRIMARY KEY (`notification_id`),
  ADD KEY `idx_user_id` (`user_id`);

--
-- Indexes for table `otp_codes`
--
ALTER TABLE `otp_codes`
  ADD PRIMARY KEY (`id`),
  ADD KEY `idx_email` (`email`),
  ADD KEY `idx_email_otp` (`email`,`otp_code`,`is_valid`);

--
-- Indexes for table `password_reset_tokens`
--
ALTER TABLE `password_reset_tokens`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `unique_token` (`token`),
  ADD KEY `idx_email` (`email`),
  ADD KEY `idx_expiry` (`expiry`),
  ADD KEY `idx_token` (`token`);

--
-- Indexes for table `qualifications`
--
ALTER TABLE `qualifications`
  ADD PRIMARY KEY (`qualification_id`),
  ADD KEY `idx_seeker_id` (`seeker_id`);

--
-- Indexes for table `ratings`
--
ALTER TABLE `ratings`
  ADD PRIMARY KEY (`rating_id`),
  ADD KEY `idx_rater_id` (`rater_id`),
  ADD KEY `idx_ratee_id` (`ratee_id`),
  ADD KEY `idx_job_id` (`job_id`);

--
-- Indexes for table `saved_jobs`
--
ALTER TABLE `saved_jobs`
  ADD PRIMARY KEY (`saved_job_id`),
  ADD KEY `seeker_id` (`seeker_id`),
  ADD KEY `job_id` (`job_id`);

--
-- Indexes for table `seeker_profiles`
--
ALTER TABLE `seeker_profiles`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `seeker_skills`
--
ALTER TABLE `seeker_skills`
  ADD PRIMARY KEY (`seeker_id`,`skill_id`),
  ADD KEY `idx_seeker_id` (`seeker_id`),
  ADD KEY `idx_skill_id` (`skill_id`);

--
-- Indexes for table `skills`
--
ALTER TABLE `skills`
  ADD PRIMARY KEY (`skill_id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indexes for table `verified_users`
--
ALTER TABLE `verified_users`
  ADD PRIMARY KEY (`email`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `applications`
--
ALTER TABLE `applications`
  MODIFY `application_id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=124;

--
-- AUTO_INCREMENT for table `availability`
--
ALTER TABLE `availability`
  MODIFY `availability_id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `employers`
--
ALTER TABLE `employers`
  MODIFY `employer_id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `interviews`
--
ALTER TABLE `interviews`
  MODIFY `interview_id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `jobs`
--
ALTER TABLE `jobs`
  MODIFY `job_id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `job_alerts`
--
ALTER TABLE `job_alerts`
  MODIFY `alert_id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `job_interest`
--
ALTER TABLE `job_interest`
  MODIFY `interest_id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `job_seekers`
--
ALTER TABLE `job_seekers`
  MODIFY `seeker_id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=140;

--
-- AUTO_INCREMENT for table `job_submissions`
--
ALTER TABLE `job_submissions`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `messages`
--
ALTER TABLE `messages`
  MODIFY `message_id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `notifications`
--
ALTER TABLE `notifications`
  MODIFY `notification_id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `otp_codes`
--
ALTER TABLE `otp_codes`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `password_reset_tokens`
--
ALTER TABLE `password_reset_tokens`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `qualifications`
--
ALTER TABLE `qualifications`
  MODIFY `qualification_id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `ratings`
--
ALTER TABLE `ratings`
  MODIFY `rating_id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `saved_jobs`
--
ALTER TABLE `saved_jobs`
  MODIFY `saved_job_id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `seeker_profiles`
--
ALTER TABLE `seeker_profiles`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `skills`
--
ALTER TABLE `skills`
  MODIFY `skill_id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `applications`
--
ALTER TABLE `applications`
  ADD CONSTRAINT `applications_ibfk_1` FOREIGN KEY (`job_id`) REFERENCES `jobs` (`job_id`) ON DELETE CASCADE,
  ADD CONSTRAINT `applications_ibfk_2` FOREIGN KEY (`seeker_id`) REFERENCES `job_seekers` (`seeker_id`) ON DELETE CASCADE;

--
-- Constraints for table `availability`
--
ALTER TABLE `availability`
  ADD CONSTRAINT `availability_ibfk_1` FOREIGN KEY (`employer_id`) REFERENCES `employers` (`employer_id`) ON DELETE CASCADE,
  ADD CONSTRAINT `availability_ibfk_2` FOREIGN KEY (`job_id`) REFERENCES `jobs` (`job_id`) ON DELETE CASCADE;

--
-- Constraints for table `interviews`
--
ALTER TABLE `interviews`
  ADD CONSTRAINT `interviews_ibfk_1` FOREIGN KEY (`availability_id`) REFERENCES `availability` (`availability_id`) ON DELETE CASCADE,
  ADD CONSTRAINT `interviews_ibfk_2` FOREIGN KEY (`seeker_id`) REFERENCES `job_seekers` (`seeker_id`) ON DELETE CASCADE;

--
-- Constraints for table `jobs`
--
ALTER TABLE `jobs`
  ADD CONSTRAINT `jobs_ibfk_1` FOREIGN KEY (`employer_id`) REFERENCES `employers` (`employer_id`) ON DELETE CASCADE;

--
-- Constraints for table `job_alerts`
--
ALTER TABLE `job_alerts`
  ADD CONSTRAINT `job_alerts_ibfk_1` FOREIGN KEY (`seeker_id`) REFERENCES `job_seekers` (`seeker_id`) ON DELETE CASCADE;

--
-- Constraints for table `job_interest`
--
ALTER TABLE `job_interest`
  ADD CONSTRAINT `job_interest_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `job_seekers` (`seeker_id`) ON DELETE CASCADE;

--
-- Constraints for table `job_skills`
--
ALTER TABLE `job_skills`
  ADD CONSTRAINT `job_skills_ibfk_1` FOREIGN KEY (`job_id`) REFERENCES `jobs` (`job_id`) ON DELETE CASCADE,
  ADD CONSTRAINT `job_skills_ibfk_2` FOREIGN KEY (`skill_id`) REFERENCES `skills` (`skill_id`) ON DELETE CASCADE;

--
-- Constraints for table `qualifications`
--
ALTER TABLE `qualifications`
  ADD CONSTRAINT `qualifications_ibfk_1` FOREIGN KEY (`seeker_id`) REFERENCES `job_seekers` (`seeker_id`) ON DELETE CASCADE;

--
-- Constraints for table `ratings`
--
ALTER TABLE `ratings`
  ADD CONSTRAINT `ratings_ibfk_1` FOREIGN KEY (`job_id`) REFERENCES `jobs` (`job_id`) ON DELETE CASCADE;

--
-- Constraints for table `saved_jobs`
--
ALTER TABLE `saved_jobs`
  ADD CONSTRAINT `saved_jobs_ibfk_1` FOREIGN KEY (`seeker_id`) REFERENCES `job_seekers` (`seeker_id`) ON DELETE CASCADE,
  ADD CONSTRAINT `saved_jobs_ibfk_2` FOREIGN KEY (`job_id`) REFERENCES `jobs` (`job_id`) ON DELETE CASCADE;

--
-- Constraints for table `seeker_profiles`
--
ALTER TABLE `seeker_profiles`
  ADD CONSTRAINT `seeker_profiles_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `job_seekers` (`seeker_id`) ON DELETE CASCADE;

--
-- Constraints for table `seeker_skills`
--
ALTER TABLE `seeker_skills`
  ADD CONSTRAINT `seeker_skills_ibfk_1` FOREIGN KEY (`seeker_id`) REFERENCES `job_seekers` (`seeker_id`) ON DELETE CASCADE,
  ADD CONSTRAINT `seeker_skills_ibfk_2` FOREIGN KEY (`skill_id`) REFERENCES `skills` (`skill_id`) ON DELETE CASCADE;
--
-- Database: `laravel`
--
CREATE DATABASE IF NOT EXISTS `laravel` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE `laravel`;

-- --------------------------------------------------------

--
-- Table structure for table `cache`
--

CREATE TABLE `cache` (
  `key` varchar(255) NOT NULL,
  `value` mediumtext NOT NULL,
  `expiration` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `cache_locks`
--

CREATE TABLE `cache_locks` (
  `key` varchar(255) NOT NULL,
  `owner` varchar(255) NOT NULL,
  `expiration` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `examples`
--

CREATE TABLE `examples` (
  `id` int(11) NOT NULL,
  `name` varchar(10) DEFAULT NULL,
  `address` varchar(10) DEFAULT NULL,
  `house_number` int(5) UNSIGNED DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `failed_jobs`
--

CREATE TABLE `failed_jobs` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `uuid` varchar(255) NOT NULL,
  `connection` text NOT NULL,
  `queue` text NOT NULL,
  `payload` longtext NOT NULL,
  `exception` longtext NOT NULL,
  `failed_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `jobs`
--

CREATE TABLE `jobs` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `queue` varchar(255) NOT NULL,
  `payload` longtext NOT NULL,
  `attempts` tinyint(3) UNSIGNED NOT NULL,
  `reserved_at` int(10) UNSIGNED DEFAULT NULL,
  `available_at` int(10) UNSIGNED NOT NULL,
  `created_at` int(10) UNSIGNED NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `job_batches`
--

CREATE TABLE `job_batches` (
  `id` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `total_jobs` int(11) NOT NULL,
  `pending_jobs` int(11) NOT NULL,
  `failed_jobs` int(11) NOT NULL,
  `failed_job_ids` longtext NOT NULL,
  `options` mediumtext DEFAULT NULL,
  `cancelled_at` int(11) DEFAULT NULL,
  `created_at` int(11) NOT NULL,
  `finished_at` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `migrations`
--

CREATE TABLE `migrations` (
  `id` int(10) UNSIGNED NOT NULL,
  `migration` varchar(255) NOT NULL,
  `batch` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `migrations`
--

INSERT INTO `migrations` (`id`, `migration`, `batch`) VALUES
(1, '0001_01_01_000000_create_users_table', 1),
(2, '0001_01_01_000001_create_cache_table', 1),
(3, '0001_01_01_000002_create_jobs_table', 1);

-- --------------------------------------------------------

--
-- Table structure for table `password_reset_tokens`
--

CREATE TABLE `password_reset_tokens` (
  `email` varchar(255) NOT NULL,
  `token` varchar(255) NOT NULL,
  `created_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `sessions`
--

CREATE TABLE `sessions` (
  `id` varchar(255) NOT NULL,
  `user_id` bigint(20) UNSIGNED DEFAULT NULL,
  `ip_address` varchar(45) DEFAULT NULL,
  `user_agent` text DEFAULT NULL,
  `payload` longtext NOT NULL,
  `last_activity` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `sessions`
--

INSERT INTO `sessions` (`id`, `user_id`, `ip_address`, `user_agent`, `payload`, `last_activity`) VALUES
('uogV9kygAjYg4AUK2htVK6r74NcZ6K07xtJb9XKy', NULL, '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36', 'YTozOntzOjY6Il90b2tlbiI7czo0MDoic3BnWDlHRVZ6dThidGoyeFRqRnZZSG5vajU1MzhJdGppak1sYUVlTyI7czo5OiJfcHJldmlvdXMiO2E6MTp7czozOiJ1cmwiO3M6MjY6Imh0dHA6Ly9maXJzdF93ZWIudGVzdC9kYXRhIjt9czo2OiJfZmxhc2giO2E6Mjp7czozOiJvbGQiO2E6MDp7fXM6MzoibmV3IjthOjA6e319fQ==', 1738554974);

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `name` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `email_verified_at` timestamp NULL DEFAULT NULL,
  `password` varchar(255) NOT NULL,
  `remember_token` varchar(100) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT NULL,
  `updated_at` timestamp NULL DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `cache`
--
ALTER TABLE `cache`
  ADD PRIMARY KEY (`key`);

--
-- Indexes for table `cache_locks`
--
ALTER TABLE `cache_locks`
  ADD PRIMARY KEY (`key`);

--
-- Indexes for table `examples`
--
ALTER TABLE `examples`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `failed_jobs`
--
ALTER TABLE `failed_jobs`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `failed_jobs_uuid_unique` (`uuid`);

--
-- Indexes for table `jobs`
--
ALTER TABLE `jobs`
  ADD PRIMARY KEY (`id`),
  ADD KEY `jobs_queue_index` (`queue`);

--
-- Indexes for table `job_batches`
--
ALTER TABLE `job_batches`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `migrations`
--
ALTER TABLE `migrations`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `password_reset_tokens`
--
ALTER TABLE `password_reset_tokens`
  ADD PRIMARY KEY (`email`);

--
-- Indexes for table `sessions`
--
ALTER TABLE `sessions`
  ADD PRIMARY KEY (`id`),
  ADD KEY `sessions_user_id_index` (`user_id`),
  ADD KEY `sessions_last_activity_index` (`last_activity`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `users_email_unique` (`email`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `examples`
--
ALTER TABLE `examples`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `failed_jobs`
--
ALTER TABLE `failed_jobs`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `jobs`
--
ALTER TABLE `jobs`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `migrations`
--
ALTER TABLE `migrations`
  MODIFY `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT;
--
-- Database: `movie`
--
CREATE DATABASE IF NOT EXISTS `movie` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE `movie`;

-- --------------------------------------------------------

--
-- Table structure for table `movies`
--

CREATE TABLE `movies` (
  `id` int(11) NOT NULL,
  `movie_name` varchar(50) NOT NULL,
  `date` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `movies`
--

INSERT INTO `movies` (`id`, `movie_name`, `date`) VALUES
(3, 'herllo', '2025-06-02');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `movies`
--
ALTER TABLE `movies`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `movies`
--
ALTER TABLE `movies`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;
--
-- Database: `phpmyadmin`
--
CREATE DATABASE IF NOT EXISTS `phpmyadmin` DEFAULT CHARACTER SET utf8 COLLATE utf8_bin;
USE `phpmyadmin`;

-- --------------------------------------------------------

--
-- Table structure for table `pma__bookmark`
--

CREATE TABLE `pma__bookmark` (
  `id` int(10) UNSIGNED NOT NULL,
  `dbase` varchar(255) NOT NULL DEFAULT '',
  `user` varchar(255) NOT NULL DEFAULT '',
  `label` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '',
  `query` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='Bookmarks';

-- --------------------------------------------------------

--
-- Table structure for table `pma__central_columns`
--

CREATE TABLE `pma__central_columns` (
  `db_name` varchar(64) NOT NULL,
  `col_name` varchar(64) NOT NULL,
  `col_type` varchar(64) NOT NULL,
  `col_length` text DEFAULT NULL,
  `col_collation` varchar(64) NOT NULL,
  `col_isNull` tinyint(1) NOT NULL,
  `col_extra` varchar(255) DEFAULT '',
  `col_default` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='Central list of columns';

-- --------------------------------------------------------

--
-- Table structure for table `pma__column_info`
--

CREATE TABLE `pma__column_info` (
  `id` int(5) UNSIGNED NOT NULL,
  `db_name` varchar(64) NOT NULL DEFAULT '',
  `table_name` varchar(64) NOT NULL DEFAULT '',
  `column_name` varchar(64) NOT NULL DEFAULT '',
  `comment` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '',
  `mimetype` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT '',
  `transformation` varchar(255) NOT NULL DEFAULT '',
  `transformation_options` varchar(255) NOT NULL DEFAULT '',
  `input_transformation` varchar(255) NOT NULL DEFAULT '',
  `input_transformation_options` varchar(255) NOT NULL DEFAULT ''
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='Column information for phpMyAdmin';

-- --------------------------------------------------------

--
-- Table structure for table `pma__designer_settings`
--

CREATE TABLE `pma__designer_settings` (
  `username` varchar(64) NOT NULL,
  `settings_data` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='Settings related to Designer';

-- --------------------------------------------------------

--
-- Table structure for table `pma__export_templates`
--

CREATE TABLE `pma__export_templates` (
  `id` int(5) UNSIGNED NOT NULL,
  `username` varchar(64) NOT NULL,
  `export_type` varchar(10) NOT NULL,
  `template_name` varchar(64) NOT NULL,
  `template_data` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='Saved export templates';

-- --------------------------------------------------------

--
-- Table structure for table `pma__favorite`
--

CREATE TABLE `pma__favorite` (
  `username` varchar(64) NOT NULL,
  `tables` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='Favorite tables';

-- --------------------------------------------------------

--
-- Table structure for table `pma__history`
--

CREATE TABLE `pma__history` (
  `id` bigint(20) UNSIGNED NOT NULL,
  `username` varchar(64) NOT NULL DEFAULT '',
  `db` varchar(64) NOT NULL DEFAULT '',
  `table` varchar(64) NOT NULL DEFAULT '',
  `timevalue` timestamp NOT NULL DEFAULT current_timestamp(),
  `sqlquery` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='SQL history for phpMyAdmin';

-- --------------------------------------------------------

--
-- Table structure for table `pma__navigationhiding`
--

CREATE TABLE `pma__navigationhiding` (
  `username` varchar(64) NOT NULL,
  `item_name` varchar(64) NOT NULL,
  `item_type` varchar(64) NOT NULL,
  `db_name` varchar(64) NOT NULL,
  `table_name` varchar(64) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='Hidden items of navigation tree';

-- --------------------------------------------------------

--
-- Table structure for table `pma__pdf_pages`
--

CREATE TABLE `pma__pdf_pages` (
  `db_name` varchar(64) NOT NULL DEFAULT '',
  `page_nr` int(10) UNSIGNED NOT NULL,
  `page_descr` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL DEFAULT ''
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='PDF relation pages for phpMyAdmin';

-- --------------------------------------------------------

--
-- Table structure for table `pma__recent`
--

CREATE TABLE `pma__recent` (
  `username` varchar(64) NOT NULL,
  `tables` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='Recently accessed tables';

--
-- Dumping data for table `pma__recent`
--

INSERT INTO `pma__recent` (`username`, `tables`) VALUES
('root', '[{\"db\":\"movie\",\"table\":\"movies\"},{\"db\":\"students\",\"table\":\"student\"},{\"db\":\"employee\",\"table\":\"employees\"},{\"db\":\"book_management\",\"table\":\"books\"},{\"db\":\"product_management\",\"table\":\"products\"},{\"db\":\"job_portal_db\",\"table\":\"job_seekers\"},{\"db\":\"basics\",\"table\":\"users\"},{\"db\":\"laravel\",\"table\":\"users\"},{\"db\":\"demo_db\",\"table\":\"task\"},{\"db\":\"job_portal_db\",\"table\":\"job_interest\"}]');

-- --------------------------------------------------------

--
-- Table structure for table `pma__relation`
--

CREATE TABLE `pma__relation` (
  `master_db` varchar(64) NOT NULL DEFAULT '',
  `master_table` varchar(64) NOT NULL DEFAULT '',
  `master_field` varchar(64) NOT NULL DEFAULT '',
  `foreign_db` varchar(64) NOT NULL DEFAULT '',
  `foreign_table` varchar(64) NOT NULL DEFAULT '',
  `foreign_field` varchar(64) NOT NULL DEFAULT ''
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='Relation table';

-- --------------------------------------------------------

--
-- Table structure for table `pma__savedsearches`
--

CREATE TABLE `pma__savedsearches` (
  `id` int(5) UNSIGNED NOT NULL,
  `username` varchar(64) NOT NULL DEFAULT '',
  `db_name` varchar(64) NOT NULL DEFAULT '',
  `search_name` varchar(64) NOT NULL DEFAULT '',
  `search_data` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='Saved searches';

-- --------------------------------------------------------

--
-- Table structure for table `pma__table_coords`
--

CREATE TABLE `pma__table_coords` (
  `db_name` varchar(64) NOT NULL DEFAULT '',
  `table_name` varchar(64) NOT NULL DEFAULT '',
  `pdf_page_number` int(11) NOT NULL DEFAULT 0,
  `x` float UNSIGNED NOT NULL DEFAULT 0,
  `y` float UNSIGNED NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='Table coordinates for phpMyAdmin PDF output';

-- --------------------------------------------------------

--
-- Table structure for table `pma__table_info`
--

CREATE TABLE `pma__table_info` (
  `db_name` varchar(64) NOT NULL DEFAULT '',
  `table_name` varchar(64) NOT NULL DEFAULT '',
  `display_field` varchar(64) NOT NULL DEFAULT ''
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='Table information for phpMyAdmin';

-- --------------------------------------------------------

--
-- Table structure for table `pma__table_uiprefs`
--

CREATE TABLE `pma__table_uiprefs` (
  `username` varchar(64) NOT NULL,
  `db_name` varchar(64) NOT NULL,
  `table_name` varchar(64) NOT NULL,
  `prefs` text NOT NULL,
  `last_update` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='Tables'' UI preferences';

--
-- Dumping data for table `pma__table_uiprefs`
--

INSERT INTO `pma__table_uiprefs` (`username`, `db_name`, `table_name`, `prefs`, `last_update`) VALUES
('root', 'job_portal_db', 'job_seekers', '{\"CREATE_TIME\":\"2025-03-21 13:30:32\",\"col_order\":[0,1,2,3,4,5,6,7,8,9,10,11],\"col_visib\":[1,1,1,1,1,1,1,1,1,1,1,1]}', '2025-05-14 01:40:04');

-- --------------------------------------------------------

--
-- Table structure for table `pma__tracking`
--

CREATE TABLE `pma__tracking` (
  `db_name` varchar(64) NOT NULL,
  `table_name` varchar(64) NOT NULL,
  `version` int(10) UNSIGNED NOT NULL,
  `date_created` datetime NOT NULL,
  `date_updated` datetime NOT NULL,
  `schema_snapshot` text NOT NULL,
  `schema_sql` text DEFAULT NULL,
  `data_sql` longtext DEFAULT NULL,
  `tracking` set('UPDATE','REPLACE','INSERT','DELETE','TRUNCATE','CREATE DATABASE','ALTER DATABASE','DROP DATABASE','CREATE TABLE','ALTER TABLE','RENAME TABLE','DROP TABLE','CREATE INDEX','DROP INDEX','CREATE VIEW','ALTER VIEW','DROP VIEW') DEFAULT NULL,
  `tracking_active` int(1) UNSIGNED NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='Database changes tracking for phpMyAdmin';

-- --------------------------------------------------------

--
-- Table structure for table `pma__userconfig`
--

CREATE TABLE `pma__userconfig` (
  `username` varchar(64) NOT NULL,
  `timevalue` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `config_data` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='User preferences storage for phpMyAdmin';

--
-- Dumping data for table `pma__userconfig`
--

INSERT INTO `pma__userconfig` (`username`, `timevalue`, `config_data`) VALUES
('root', '2025-06-03 12:44:11', '{\"Console\\/Mode\":\"collapse\",\"ThemeDefault\":\"metro\"}');

-- --------------------------------------------------------

--
-- Table structure for table `pma__usergroups`
--

CREATE TABLE `pma__usergroups` (
  `usergroup` varchar(64) NOT NULL,
  `tab` varchar(64) NOT NULL,
  `allowed` enum('Y','N') NOT NULL DEFAULT 'N'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='User groups with configured menu items';

-- --------------------------------------------------------

--
-- Table structure for table `pma__users`
--

CREATE TABLE `pma__users` (
  `username` varchar(64) NOT NULL,
  `usergroup` varchar(64) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin COMMENT='Users and their assignments to user groups';

--
-- Indexes for dumped tables
--

--
-- Indexes for table `pma__bookmark`
--
ALTER TABLE `pma__bookmark`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `pma__central_columns`
--
ALTER TABLE `pma__central_columns`
  ADD PRIMARY KEY (`db_name`,`col_name`);

--
-- Indexes for table `pma__column_info`
--
ALTER TABLE `pma__column_info`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `db_name` (`db_name`,`table_name`,`column_name`);

--
-- Indexes for table `pma__designer_settings`
--
ALTER TABLE `pma__designer_settings`
  ADD PRIMARY KEY (`username`);

--
-- Indexes for table `pma__export_templates`
--
ALTER TABLE `pma__export_templates`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `u_user_type_template` (`username`,`export_type`,`template_name`);

--
-- Indexes for table `pma__favorite`
--
ALTER TABLE `pma__favorite`
  ADD PRIMARY KEY (`username`);

--
-- Indexes for table `pma__history`
--
ALTER TABLE `pma__history`
  ADD PRIMARY KEY (`id`),
  ADD KEY `username` (`username`,`db`,`table`,`timevalue`);

--
-- Indexes for table `pma__navigationhiding`
--
ALTER TABLE `pma__navigationhiding`
  ADD PRIMARY KEY (`username`,`item_name`,`item_type`,`db_name`,`table_name`);

--
-- Indexes for table `pma__pdf_pages`
--
ALTER TABLE `pma__pdf_pages`
  ADD PRIMARY KEY (`page_nr`),
  ADD KEY `db_name` (`db_name`);

--
-- Indexes for table `pma__recent`
--
ALTER TABLE `pma__recent`
  ADD PRIMARY KEY (`username`);

--
-- Indexes for table `pma__relation`
--
ALTER TABLE `pma__relation`
  ADD PRIMARY KEY (`master_db`,`master_table`,`master_field`),
  ADD KEY `foreign_field` (`foreign_db`,`foreign_table`);

--
-- Indexes for table `pma__savedsearches`
--
ALTER TABLE `pma__savedsearches`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `u_savedsearches_username_dbname` (`username`,`db_name`,`search_name`);

--
-- Indexes for table `pma__table_coords`
--
ALTER TABLE `pma__table_coords`
  ADD PRIMARY KEY (`db_name`,`table_name`,`pdf_page_number`);

--
-- Indexes for table `pma__table_info`
--
ALTER TABLE `pma__table_info`
  ADD PRIMARY KEY (`db_name`,`table_name`);

--
-- Indexes for table `pma__table_uiprefs`
--
ALTER TABLE `pma__table_uiprefs`
  ADD PRIMARY KEY (`username`,`db_name`,`table_name`);

--
-- Indexes for table `pma__tracking`
--
ALTER TABLE `pma__tracking`
  ADD PRIMARY KEY (`db_name`,`table_name`,`version`);

--
-- Indexes for table `pma__userconfig`
--
ALTER TABLE `pma__userconfig`
  ADD PRIMARY KEY (`username`);

--
-- Indexes for table `pma__usergroups`
--
ALTER TABLE `pma__usergroups`
  ADD PRIMARY KEY (`usergroup`,`tab`,`allowed`);

--
-- Indexes for table `pma__users`
--
ALTER TABLE `pma__users`
  ADD PRIMARY KEY (`username`,`usergroup`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `pma__bookmark`
--
ALTER TABLE `pma__bookmark`
  MODIFY `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `pma__column_info`
--
ALTER TABLE `pma__column_info`
  MODIFY `id` int(5) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `pma__export_templates`
--
ALTER TABLE `pma__export_templates`
  MODIFY `id` int(5) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `pma__history`
--
ALTER TABLE `pma__history`
  MODIFY `id` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `pma__pdf_pages`
--
ALTER TABLE `pma__pdf_pages`
  MODIFY `page_nr` int(10) UNSIGNED NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `pma__savedsearches`
--
ALTER TABLE `pma__savedsearches`
  MODIFY `id` int(5) UNSIGNED NOT NULL AUTO_INCREMENT;
--
-- Database: `product_management`
--
CREATE DATABASE IF NOT EXISTS `product_management` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE `product_management`;

-- --------------------------------------------------------

--
-- Table structure for table `products`
--

CREATE TABLE `products` (
  `id` int(11) NOT NULL,
  `product_name` varchar(50) NOT NULL,
  `price` int(5) NOT NULL,
  `created_at` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `products`
--
ALTER TABLE `products`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `products`
--
ALTER TABLE `products`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=74;
--
-- Database: `students`
--
CREATE DATABASE IF NOT EXISTS `students` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE `students`;

-- --------------------------------------------------------

--
-- Table structure for table `student`
--

CREATE TABLE `student` (
  `id` int(11) NOT NULL,
  `student` varchar(50) NOT NULL,
  `date` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `student`
--

INSERT INTO `student` (`id`, `student`, `date`) VALUES
(3, 'e', '2025-06-02');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `student`
--
ALTER TABLE `student`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `student`
--
ALTER TABLE `student`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;
--
-- Database: `test`
--
CREATE DATABASE IF NOT EXISTS `test` DEFAULT CHARACTER SET latin1 COLLATE latin1_swedish_ci;
USE `test`;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
