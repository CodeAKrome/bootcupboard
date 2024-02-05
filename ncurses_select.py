#!env python3

import curses


def select_model(stdscr, models):
    curses.curs_set(0)
    current_row = 0

    while 1:
        stdscr.clear()
        h, w = stdscr.getmaxyx()

        for idx, row in enumerate(models):
            x = w // 2 - len(row) // 2
            y = h // 2 - len(models) // 2 + idx
            if idx == current_row:
                stdscr.attron(curses.color_pair(1))
                stdscr.addstr(y, x, row)
                stdscr.attroff(curses.color_pair(1))
            else:
                stdscr.addstr(y, x, row)

        key = stdscr.getch()

        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(models) - 1:
            current_row += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            return models[current_row]

        stdscr.refresh()


def main():
    models = [
        "gpt-4",
        "gpt-3.5-turbo",
        "gpt-3.5-turbo-16k",
        "togethercomputer/llama-2-70b-chat",
        "togethercomputer/llama-2-70b",
        "togethercomputer/LLaMA-2-7B-32K",
        "togethercomputer/Llama-2-7B-32K-Instruct",
        "togethercomputer/llama-2-7b",
        "togethercomputer/CodeLlama-34b",
        "WizardLM/WizardCoder-Python-34B-V1.0",
        "NousResearch/Nous-Hermes-Llama2-13b",
        "togethercomputer/falcon-40b-instruct",
        "togethercomputer/falcon-7b-instruct",
        "j2-ultra",
        "j2-mid",
        "j2-light",
        "dolpin",
        "chatdolphin",
        "claude-2",
        "claude-instant-v1",
    ]

    selected_model = curses.wrapper(select_model, models)
    print(f"export HACKMOD='openai/{selected_model}'; poetry run interpreter")


if __name__ == "__main__":
    main()
