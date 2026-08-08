<?php
require_once __DIR__ . '/auth.php';

if (current_user()) {
    header('Location: index.php');
    exit;
}

$error = '';
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $username = $_POST['username'] ?? '';
    $password = $_POST['password'] ?? '';

    $db = get_db();

    $query = "SELECT id, username, is_admin FROM users WHERE username = '$username' AND password = '$password'";

    try {
        $result = $db->query($query);
        $user   = $result ? $result->fetch(PDO::FETCH_ASSOC) : false;
    } catch (\PDOException $e) {
        $user = false;
    }

    if ($user) {
        $_SESSION['user_id'] = $user['id'];
        header('Location: index.php');
        exit;
    }
    $error = 'Napačno uporabniško ime ali geslo.';
}

include __DIR__ . '/includes/header.php';
?>
<h1>Prijava</h1>
<?php if ($error): ?><p class="error"><?= h($error) ?></p><?php endif; ?>
<form method="post">
  <label>Uporabniško ime</label>
  <input type="text" name="username" required>
  <label>Geslo</label>
  <input type="password" name="password" required>
  <button type="submit">Prijava</button>
</form>
<p class="dim">Novi uporabniki se ne morejo samostojno registrirati — za dostop se obrnite na skrbnika.</p>
<?php include __DIR__ . '/includes/footer.php'; ?>
