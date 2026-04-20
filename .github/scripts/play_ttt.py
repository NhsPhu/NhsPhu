import os
import sys
import re
import random

def check_winner(board, player):
    win_lines = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],
        [0, 3, 6], [1, 4, 7], [2, 5, 8],
        [0, 4, 8], [2, 4, 6]
    ]
    for line in win_lines:
        if all(board[i] == player for i in line):
            return True
    return False

def render_board(board, game_over):
    lines = []
    lines.append("|   | 1 | 2 | 3 |")
    lines.append("|---|---|---|---|")
    rows = ["A", "B", "C"]
    repo = os.environ.get("GITHUB_REPOSITORY", "NhsPhu/NhsPhu")
    url_template = f"https://github.com/{repo}/issues/new?title=ttt%7C{{index}}&body=Bam+Submit+new+issue+de+di+nuoc+co+nay."
    
    for i in range(3):
        row_str = f"| **{rows[i]}** |"
        for j in range(3):
            idx = i * 3 + j
            if board[idx] == 'X':
                row_str += " ❌ |"
            elif board[idx] == 'O':
                row_str += " ⭕ |"
            else:
                if game_over:
                    # Chơi xong thì không cho bấm nữa
                    row_str += " ⬜ |"
                else:
                    row_str += f" [<kbd>⬜</kbd>]({url_template.format(index=idx)}) |"
        lines.append(row_str)
    return "\n".join(lines)

def main():
    if len(sys.argv) < 2:
        return
        
    title = sys.argv[1].strip()
    if not title.startswith("ttt|"):
        return

    repo = os.environ.get("GITHUB_REPOSITORY", "NhsPhu/NhsPhu")
    
    with open("README.md", "r", encoding="utf-8") as f:
        readme = f.read()
        
    state_match = re.search(r'<!-- ttt_state: (.{9}) -->', readme)
    board = list(state_match.group(1)) if state_match else [' '] * 9

    status_msg = "**Đến lượt của bạn! Nhấn vào một ô màu trắng để đi (X).**"
    game_over = False
    
    if title == "ttt|reset":
        board = [' '] * 9
    else:
        try:
            move = int(title.split("|")[1])
        except ValueError:
            return
            
        if move < 0 or move > 8 or board[move] != ' ':
            return # Nuoc di khong hop le
            
        board[move] = 'X'
        
        if check_winner(board, 'X'):
            status_msg = "**🎉 TADA! Bạn đã thắng xuất sắc! 🎉**"
            game_over = True
        elif ' ' not in board:
            status_msg = "**🤝 Hòa rồi! Bất phân thắng bại! 🤝**"
            game_over = True
        else:
            bot_move = random.choice([i for i, v in enumerate(board) if v == ' '])
            board[bot_move] = 'O'
            
            if check_winner(board, 'O'):
                status_msg = "**💀 Haha, máy tính (O) đã thắng! Thử lại nhé! 💀**"
                game_over = True
            elif ' ' not in board:
                status_msg = "**🤝 Hòa rồi! Bất phân thắng bại! 🤝**"
                game_over = True

    if game_over:
        status_msg += f"\n\n[🔄 Bấm vào đây để chơi lại ván mới](https://github.com/{repo}/issues/new?title=ttt%7Creset&body=Submit+issue+nay+de+lam+van+moi)"

    state_str = "".join(board)
    board_md = render_board(board, game_over)
    
    new_readme = re.sub(
        r'<!-- ttt_start -->.*<!-- ttt_end -->',
        f'<!-- ttt_start -->\n{status_msg}\n\n{board_md}\n\n<!-- ttt_state: {state_str} -->\n<!-- ttt_end -->',
        readme,
        flags=re.DOTALL
    )
    
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(new_readme)

if __name__ == "__main__":
    main()
