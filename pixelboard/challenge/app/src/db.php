<?php

function get_db(): PDO
{
    static $db = null;
    if ($db !== null) {
        return $db;
    }

    $dbPath = '/var/www/data/forum.db';
    $isNew  = !file_exists($dbPath);

    $db = new PDO('sqlite:' . $dbPath);
    $db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

    if ($isNew) {
        $db->exec('
            CREATE TABLE users (
                id       INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                is_admin INTEGER NOT NULL DEFAULT 0,
                avatar   TEXT NOT NULL DEFAULT \'default.png\'
            );
            CREATE TABLE posts (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id    INTEGER NOT NULL,
                title      TEXT NOT NULL,
                body       TEXT NOT NULL,
                image      TEXT,
                created_at TEXT NOT NULL
            );
            CREATE TABLE comments (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                post_id    INTEGER NOT NULL,
                user_id    INTEGER NOT NULL,
                body       TEXT NOT NULL,
                created_at TEXT NOT NULL
            );
        ');

        $adminPassword = getenv('ADMIN_PASSWORD') ?: bin2hex(random_bytes(16));
        $stmt = $db->prepare(
            'INSERT INTO users (username, password, is_admin, avatar) VALUES (\'admin\', :pw, 1, :avatar)'
        );
        $stmt->execute([':pw' => $adminPassword, ':avatar' => 'avatar-admin.png']);

        // A handful of regular (non-admin) community members, each with a
        // random password and its own avatar, so the forum doesn't look
        // empty (or like everyone shares one profile picture) on first boot.
        $randomUsernames = ['ana_lens', 'miha_snap', 'urska_photo', 'luka_focus', 'nika_frames'];
        $userStmt = $db->prepare(
            'INSERT INTO users (username, password, is_admin, avatar) VALUES (:username, :pw, 0, :avatar)'
        );
        $userIds = [1];
        foreach ($randomUsernames as $username) {
            $userStmt->execute([
                ':username' => $username,
                ':pw'       => bin2hex(random_bytes(8)),
                ':avatar'   => "avatar-{$username}.png",
            ]);
            $userIds[] = (int)$db->lastInsertId();
        }

        $postStmt = $db->prepare(
            'INSERT INTO posts (user_id, title, body, image, created_at) VALUES (:uid, :title, :body, :image, :ts)'
        );
        $seedPosts = [
            [1, 'Dobrodošli na PixelBoard!', "Delite svoje najboljše fotografije z ostalimi člani skupnosti.\nNe pozabite si nastaviti profilne slike v svojem profilu!", null],
            [$userIds[1], 'Sončni zahod nad Triglavom', 'Včeraj sem ujela čudovit zahod sonca na poti proti Kredarici. Barve so bile neverjetne!', 'seed-sunset.png'],
            [$userIds[2], 'Ulična fotografija v Ljubljani', 'Preizkušam nov objektiv 35mm na Prešernovem trgu. Kakšni nasveti za street photography?', 'seed-street.png'],
            [$userIds[3], 'Makro fotografija žuželk', 'Konjenice se lovim v vrtu že cel teden. Potrebujem boljši macro objektiv priporočila?', 'seed-macro.png'],
            [$userIds[4], 'Nočno fotografiranje zvezd', 'Postavil sem stativ na Krvavcu in poskusil dolgo osvetlitev. Rezultat je bil vreden čakanja.', 'seed-stars.png'],
            [$userIds[5], 'Portreti ob zlati uri', 'Najboljša svetloba za portrete je res tik pred sončnim zahodom. Deljenje mojih najljubših kadrov.', 'seed-portrait.png'],
        ];
        foreach ($seedPosts as $i => [$uid, $title, $body, $image]) {
            $postStmt->execute([
                ':uid'   => $uid,
                ':title' => $title,
                ':body'  => $body,
                ':image' => $image,
                ':ts'    => date('c', time() - (count($seedPosts) - $i) * 3600),
            ]);
        }

        $commentStmt = $db->prepare(
            'INSERT INTO comments (post_id, user_id, body, created_at) VALUES (:pid, :uid, :body, :ts)'
        );
        $seedComments = [
            [2, $userIds[2], 'Čudovite barve, kje točno si stala?'],
            [2, $userIds[3], 'Krasen posnetek, mi je res všeč kompozicija.'],
            [3, $userIds[4], '35mm je odličen izbor za ulično fotografijo, uživaj!'],
            [4, $userIds[5], 'Poskusi z reverse ringom, deluje presenetljivo dobro.'],
            [5, $userIds[1], 'Zvezdno nebo na Krvavcu je res nekaj posebnega.'],
        ];
        foreach ($seedComments as $c) {
            [$pid, $uid, $body] = $c;
            $commentStmt->execute([
                ':pid'  => $pid,
                ':uid'  => $uid,
                ':body' => $body,
                ':ts'   => date('c'),
            ]);
        }
    }

    return $db;
}
