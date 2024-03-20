#!/usr/bin/python3 -B
from .downloader import show_stuff
import argparse
import logging
import os
import validators
from .parser import RoosterTeethParser
from pathlib import Path
import random


log_dir = Path.cwd() / "logs"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)


def load_slugs_from_downloaded_log():
    downloaded_log_path = Path.cwd() / "logs" / "downloaded.log"
    slugs = set()

    if os.path.isfile(downloaded_log_path):
        try:
            with open(downloaded_log_path, "r") as f:
                for line in f:
                    slugs.add(
                        line.strip()
                    )  # Assuming each line in the log file represents a slug
        except (FileNotFoundError, IOError) as err:
            logging.warning("Error for opening Slugs: {err}")
            pass
    print("Loaded all previously downloaded slug...")
    return slugs


logging.basicConfig(
    filename="logs/rooster.log",
    filemode="a",
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.DEBUG,
)


def process_links_from_file(
    username,
    password,
    filename,
    concurrent_fragments,
    fast_check,
    use_aria,
    fn_mode,
    fragment_retries,
    fragment_abort,
    total_slugs,
    ignore_existing,
    keep_after_upload,
    update_metadata,
    randomize,
):
    with open(filename, "r") as file:
        links = file.readlines()
        num_links = len(links)
        print(f"Found {num_links} links.")
        if randomize:
            print(f"Shuffling the list of {num_links} links. *shakes very violently*")
            random.shuffle(links)

    for index, line in enumerate(links, start=1):
        print(f"Downloading link {index} of {num_links}: {line.strip()}")
        try:
            show_stuff(
                username,
                password,
                line.strip(),
                concurrent_fragments,
                fast_check,
                use_aria,
                fn_mode,
                fragment_retries,
                fragment_abort,
                total_slugs,
                ignore_existing,
                keep_after_upload,
                update_metadata,
            )
        except Exception as e:
            # Log the exception
            print(f"Error occurred while processing link {index}: {line.strip()}")
            logging.critical(
                f"{e} - Error occurred while processing link {index}: {line.strip()}"
            )


def process_links_from_list(
    username,
    password,
    episode_links,
    concurrent_fragments,
    input_value,
    fast_check,
    use_aria,
    fn_mode,
    fragment_retries,
    fragment_abort,
    total_slugs,
    ignore_existing,
    keep_after_upload,
    update_metadata,
    randomize,
):
    num_links = len(episode_links)
    if randomize:
        print(f"Shuffling the list of {num_links} links. *shakes very violently*")
        random.shuffle(episode_links)

    for index, episode in enumerate(episode_links):
        print(f"Downloading link {index+1} of {num_links}: {episode}")
        try:
            show_stuff(
                username,
                password,
                episode,
                concurrent_fragments,
                fast_check,
                use_aria,
                fn_mode,
                fragment_retries,
                fragment_abort,
                total_slugs,
                ignore_existing,
                keep_after_upload,
                update_metadata,
            )
        except Exception as e:
            # Log the exception
            print(
                f"{e} Error occurred while processing link {index+1}: {episode} | Input : {input_value}"
            )
            logging.critical(
                f"{e} Error occurred while processing link {index+1}: {episode} | Input: {input_value}"
            )


def main():
    parser = argparse.ArgumentParser(description="Process command line arguments")

    parser.add_argument("--email", help="Email for authentication")
    parser.add_argument("--password", help="Password for authentication")
    parser.add_argument(
        "--concurrent-fragments",
        default=10,
        type=int,
        help="Number of concurrent fragments (default is 10)",
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--show", action="store_true", help="Download in a Predefied Show formatting"
    )
    group.add_argument(
        "--ia", action="store_true", help="Upload to IA and delete uploaded file"
    )

    group.add_argument(
        "--archivist",
        action="store_true",
        help="Downloads in a Archivist like fashion",
    )

    parser.add_argument(
        "--fast-check",
        action="store_true",
        help="Enable Fast check for already downlaoded links",
    )
    parser.add_argument(
        "--use-aria",
        action="store_true",
        help="Use aria2c as downloader if it exists in system",
    )
    parser.add_argument(
        "--i",
        action="store_true",
        help="Ignore exisitng uploads",
    )

    parser.add_argument(
        "--keep-uploads",
        action="store_true",
        help="Do not delete files after uploads",
    )

    parser.add_argument(
        "--update-meta",
        action="store_true",
        help="Only update metadata, nothing else",
    )

    parser.add_argument(
        "--fragment-retries",
        default=10,
        type=int,
        help="Number of attempts to retry downloading fragments (default is 10)",
    )
    parser.add_argument(
        "--fragment-abort",
        action="store_false",
        help="Abort if fail to download fragment (default off)",
    )

    parser.add_argument(
        "--random",
        action="store_true",
        help="Randomize the links on runs if a txt file/series/season is provided",
    )

    parser.add_argument("input", help="URL or file containing list of links")

    args = parser.parse_args()
    # if args.show and args.ia:
    #     parser.error("Cannot specify both --show and --ia. Please choose one.")

    username = args.email
    password = args.password
    input_value = args.input
    concurrent_fragments = args.concurrent_fragments
    show_flag = args.show
    upload_to_ia = args.ia
    archivist_mode = args.archivist
    fast_check = args.fast_check
    use_aria = args.use_aria
    fragment_retries = args.fragment_retries
    fragment_abort = args.fragment_abort
    ignore_existing = args.i
    keep_after_upload = args.keep_uploads
    update_metadata = args.update_meta
    randomize = args.random

    if show_flag:
        fn_mode = "show"
    elif archivist_mode:
        fn_mode = "archivist"
    elif upload_to_ia:
        fn_mode = "ia"
        print(
            "Upload to IA is in beta, if you find any errors please ping @fhm on discord. id: 0.2.0b-2"
        )
        # exit()

    total_slugs = load_slugs_from_downloaded_log()

    if input_value.endswith(".txt"):
        process_links_from_file(
            username,
            password,
            input_value,
            concurrent_fragments,
            fast_check,
            use_aria,
            fn_mode,
            fragment_retries,
            fragment_abort,
            total_slugs,
            ignore_existing,
            keep_after_upload,
            update_metadata,
            randomize,
        )
    else:
        if validators.url(input_value):
            url_parts = input_value.split("/")
            if "roosterteeth.com" in url_parts and "series" in url_parts:
                parser = RoosterTeethParser()
                episode_links = parser.get_episode_links(input_value)
                if episode_links is not None:
                    process_links_from_list(
                        username,
                        password,
                        episode_links,
                        concurrent_fragments,
                        input_value,
                        fast_check,
                        use_aria,
                        fn_mode,
                        fragment_retries,
                        fragment_abort,
                        total_slugs,
                        ignore_existing,
                        keep_after_upload,
                        update_metadata,
                        randomize,
                    )
                else:
                    print(
                        f"something went wrong with parsing: {input_value}. Try again or check your links"
                    )
                    logging.critical(f"parsing failed for: {input_value}")
                    exit()

            elif "roosterteeth.com" in url_parts and "watch" in url_parts:
                show_stuff(
                    username=username,
                    password=password,
                    vod_url=input_value,
                    concurrent_fragments=concurrent_fragments,
                    fast_check=fast_check,
                    use_aria=use_aria,
                    fn_mode=fn_mode,
                    fragment_retries=fragment_retries,
                    fragment_abort=fragment_abort,
                    total_slugs=total_slugs,
                    ignore_existing=ignore_existing,
                    keep_after_upload=keep_after_upload,
                    update_metadata=update_metadata,
                )
            else:
                print("Unsupported RT URL. Only supports Series and Episodes")
                logging.warning(
                    f"{input_value}-  Unsupported RT URL. Only supports Series and Episodes"
                )
                exit()
        else:
            print(f"invalid url: {input_value}. Exiting.")
            logging.warning(f"invalid url: {input_value}. Exiting.")
            exit()


if __name__ == "__main__":
    raise SystemExit(main())
