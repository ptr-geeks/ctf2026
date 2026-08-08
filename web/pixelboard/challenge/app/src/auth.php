<?php

session_start();
require_once __DIR__ . '/db.php';

function current_user(): ?array
{
    static $cache = false;
    if ($cache !== false) {
        return $cache;
    }
    if (!isset($_SESSION['user_id'])) {
        $cache = null;
        return $cache;
    }
    $db   = get_db();
    $stmt = $db->prepare('SELECT id, username, is_admin, avatar FROM users WHERE id = :id');
    $stmt->execute([':id' => $_SESSION['user_id']]);
    $user  = $stmt->fetch(PDO::FETCH_ASSOC);
    $cache = $user ?: null;
    return $cache;
}

function require_login(): array
{
    $user = current_user();
    if (!$user) {
        header('Location: login.php');
        exit;
    }
    return $user;
}

function h(string $s): string
{
    return htmlspecialchars($s, ENT_QUOTES, 'UTF-8');
}
