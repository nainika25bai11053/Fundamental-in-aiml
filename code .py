import streamlit as st
import random
import time

st.set_page_config(page_title="Tic Tac Toe AI", layout="centered")

# ---------------- STATE ----------------
if "board" not in st.session_state:
    st.session_state.board = [" "]*9
    st.session_state.game_over = False
    st.session_state.winner = None
    st.session_state.mode = "Player vs AI"
    st.session_state.difficulty = "Hard"
    st.session_state.last_ai_move = None
    st.session_state.last_ai_score = None
    st.session_state.history = []
    st.session_state.stats = {"You":0, "Computer":0, "Draw":0}
    st.session_state.turn = "X"

# ---------------- LOGIC ----------------
def check_winner(b, p):
    wins = [
        [0,1,2],[3,4,5],[6,7,8],
        [0,3,6],[1,4,7],[2,5,8],
        [0,4,8],[2,4,6]
    ]
    return any(all(b[i]==p for i in w) for w in wins)

def minimax(b, is_max):
    if check_winner(b,"O"): return 1
    if check_winner(b,"X"): return -1
    if " " not in b: return 0

    if is_max:
        best = -999
        for i in range(9):
            if b[i]==" ":
                b[i]="O"
                best = max(best, minimax(b, False))
                b[i]=" "
        return best
    else:
        best = 999
        for i in range(9):
            if b[i]==" ":
                b[i]="X"
                best = min(best, minimax(b, True))
                b[i]=" "
        return best

def best_move(b, difficulty):
    empty = [i for i in range(9) if b[i]==" "]

    if difficulty == "Easy":
        return random.choice(empty), 0

    if difficulty == "Medium":
        if random.random() < 0.5:
            return random.choice(empty), 0

    best = -999
    move = None

    for i in empty:
        b[i] = "O"
        score = minimax(b, False)
        b[i] = " "

        if score > best:
            best = score
            move = i

    return move, best

# ---------------- GAME ----------------
def click(i):
    if st.session_state.game_over:
        return
    if st.session_state.board[i] != " ":
        return

    st.session_state.history.append(st.session_state.board.copy())

    # PLAYER vs PLAYER
    if st.session_state.mode == "2 Player":
        st.session_state.board[i] = st.session_state.turn
        st.session_state.turn = "O" if st.session_state.turn=="X" else "X"

    # PLAYER vs AI
    else:
        st.session_state.board[i] = "X"

    # Check win (player)
    if check_winner(st.session_state.board,"X"):
        st.session_state.game_over = True
        st.session_state.winner = "You"
        st.session_state.stats["You"] += 1
        return

    if st.session_state.mode == "2 Player":
        if check_winner(st.session_state.board,"O"):
            st.session_state.game_over = True
            st.session_state.winner = "Player O"
            return

    if " " not in st.session_state.board:
        st.session_state.game_over = True
        st.session_state.winner = "Draw"
        st.session_state.stats["Draw"] += 1
        return

    # AI TURN
    if st.session_state.mode == "Player vs AI":
        time.sleep(0.5)
        ai, score = best_move(st.session_state.board, st.session_state.difficulty)

        if ai is not None:
            st.session_state.board[ai] = "O"
            st.session_state.last_ai_move = ai
            st.session_state.last_ai_score = score

        if check_winner(st.session_state.board,"O"):
            st.session_state.game_over = True
            st.session_state.winner = "Computer"
            st.session_state.stats["Computer"] += 1
            return

    if " " not in st.session_state.board:
        st.session_state.game_over = True
        st.session_state.winner = "Draw"
        st.session_state.stats["Draw"] += 1

# ---------------- UI ----------------
st.markdown("<h1 style='text-align:center;'>🎮 Tic Tac Toe AI</h1>", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    st.session_state.mode = st.selectbox("Mode", ["Player vs AI", "2 Player"])
with col2:
    st.session_state.difficulty = st.selectbox("Difficulty", ["Easy", "Medium", "Hard"])

# BOARD
for row in range(3):
    cols = st.columns(3)
    for col in range(3):
        idx = row*3 + col
        cols[col].button(
            st.session_state.board[idx],
            key=f"cell_{idx}",
            on_click=click,
            args=(idx,)
        )

# ---------------- AI EXPLANATION ----------------
if st.session_state.last_ai_move is not None and st.session_state.mode == "Player vs AI":
    score = st.session_state.last_ai_score
    if score == 1:
        msg = "AI aims to WIN 🏆"
    elif score == 0:
        msg = "AI forces a DRAW 🤝"
    else:
        msg = "AI is BLOCKING you 🚫"
    st.info(f"{msg} (Position {st.session_state.last_ai_move})")

# ---------------- RESULT ----------------
if st.session_state.game_over:
    if st.session_state.winner == "You":
        st.success("You Win 🎉")
    elif st.session_state.winner == "Computer":
        st.error("Computer Wins 🤖")
    elif st.session_state.winner == "Draw":
        st.warning("Draw 🤝")
    else:
        st.success(f"{st.session_state.winner} Wins")

# ---------------- HINT ----------------
if st.button("💡 Hint"):
    hint, _ = best_move(st.session_state.board, "Hard")
    st.warning(f"Best move is position {hint}")

# ---------------- UNDO ----------------
if st.button("↩ Undo"):
    if st.session_state.history:
        st.session_state.board = st.session_state.history.pop()
        st.session_state.game_over = False

# ---------------- SCORE ----------------
st.subheader("📊 Score Board")
st.write(st.session_state.stats)

# ---------------- RESET ----------------
if st.button("🔄 Restart Game"):
    st.session_state.board = [" "]*9
    st.session_state.game_over = False
    st.session_state.winner = None
    st.session_state.last_ai_move = None
