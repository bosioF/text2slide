if __name__ == "__main__":
    from backend import *
    from help import *

    def main():
        if len(sys.argv) == 2 and sys.argv[1] == "--help":
            print(HELP_MSG)
            sys.exit(0)

        if len(sys.argv) not in [4, 5]:
            print(USAGE_MSG)
            sys.exit(1)

        input_file = sys.argv[1]
        quality = sys.argv[2]
        output_file_name = sys.argv[3]
        audio_path = sys.argv[4] if len(sys.argv) == 5 else None

        check_args(input_file, quality, output_file_name)

        color = input("What color should the text be? ").strip().upper()
        validate_color(color)

        prepare_output_dirs()
        dir_name = get_dir_name(quality)
        process_video(input_file, color, output_file_name, quality, dir_name, audio_path)

    main()
