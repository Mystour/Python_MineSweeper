from selectLevel import SelectLevel


def main():
    # create the main window
    game = SelectLevel(main)

    # start the main event loop
    game.root.mainloop()


if __name__ == '__main__':
    main()
