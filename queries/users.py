async def user_exists(pool, user):
    query = '''
    select exists(select id from users where id=$1)
    '''
    conn = await pool.acquire()

    try:
        id = user.get('id')
        result = await conn.fetchval(query, id)

    finally:
        await pool.release(conn)

    return result


async def insert_user(pool, user):
    query = '''
    insert into users(id, first_name, last_name, username, is_active)
    values ($1, $2, $3, $4, $5)
    on conflict (id)
    do update set (first_name, last_name, username, is_active) = ($2, $3, $4, $5)
    '''

    conn = await pool.acquire()

    try:
        id = user.get('id')
        first_name = user.get('first_name')
        last_name = user.get('last_name', '')
        username = user.get('username', '')
        is_active = True
        await conn.execute(query, id, first_name, last_name, username, is_active)

    finally:
        await pool.release(conn)


async def deactivate_user(pool, user):
    query = '''
    update users
    set is_active=false
    where id=$1
    '''

    conn = await pool.acquire()

    try:
        id = user.get('id')
        await conn.execute(query, id)

    finally:
        await pool.release(conn)


async def user_has_draft(pool, category_id, user_id):
    query = '''
    select exists(select id from drafts where category_id=$1 and user_id=$2)
    '''

    conn = await pool.acquire()

    try:
        result = await conn.fetchval(query, category_id, user_id)

    finally:
        await pool.release(conn)

    return result


async def has_user_products(pool, user):
    query = '''
    select exists(select id from products where written_by=$1)
    '''

    conn = await pool.acquire()

    try:
        id = user.get('id')
        result = await conn.fetchval(query, id)

    finally:
        await pool.release(conn)

    return result


async def is_user_admin(pool, user):
    query = '''
    select exists(select id from users where id=$1 and is_admin is true);
    '''

    conn = await pool.acquire()

    try:
        id = user.get('id')
        result = await conn.fetchval(query, id)

    finally:
        await pool.release(conn)

    return result


async def make_user_admin(pool, username):
    query = '''
    update users
    set is_admin=true
    where username=$1
    '''

    conn = await pool.acquire()

    try:
        await conn.execute(query, username)

    finally:
        await pool.release(conn)


async def get_admins(pool):
    query = '''
    select array_agg(username) from users where is_admin=true
    '''

    conn = await pool.acquire()

    try:
        result = await conn.fetchval(query)

    finally:
        await pool.release(conn)

    return result
