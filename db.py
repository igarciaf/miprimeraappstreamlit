def create_user(nombre: str, email: str, password_hash: str, bio: Optional[str]=None, comuna: Optional[str]=None) -> int:
    conn = get_conn()
    cur = conn.cursor()
    created_at = datetime.utcnow().isoformat()
    try:
        cur.execute(
            "INSERT INTO users (nombre, email, password_hash, bio, comuna, created_at) VALUES (?, ?, ?, ?, ?, ?)",
            (nombre, email, password_hash, bio, comuna, created_at)
        )
        conn.commit()
        user_id = cur.lastrowid
    except sqlite3.IntegrityError as e:
        print("❌ Error al crear usuario:", e)
        user_id = 0
    conn.close()
    return user_id
