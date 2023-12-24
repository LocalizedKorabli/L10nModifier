import os

import polib

splitter_str = "*" * 25


def run():
    should_continue = True
    root_dir = input("请输入要被修改的mo文件的绝对路径，您可以尝试将文件直接拖入本程序运行的命令行页面以快速输入：")
    while not os.path.isfile(root_dir):
        root_dir = input("mo文件路径错误，请重新输入：")
    dir_list: list[str] = []
    while should_continue:
        new_dir = input(
            "请输入作为修改文件的绝对路径或将文件拖入本页面（输入0以结束添加文件）：")
        if new_dir == "0":
            print("结束添加修改文件。")
            break
        if os.path.isfile(new_dir):
            dir_list.append(new_dir)
            _list_current_file(root_dir, dir_list)
        else:
            print("指定的文件有误。")
    source_mo = polib.mofile(root_dir)
    for path in dir_list:
        print(f"应用{path}到{root_dir}……")
        try:
            _process_modification_file(source_mo, path)
        except Exception as ex:
            print(f"应用修改文件“{path}”时发生异常！异常信息：{ex}")

    if not os.path.exists('l10n_modifier_output'):
        os.mkdir('l10n_modifier_output')
    source_mo.save_as_pofile('l10n_modifier_output/merged.po')
    source_mo.save('l10n_modifier_output/merged.mo')
    input("已将修改后的po、mo文件保存到l10n_modifier_output文件夹下，按回车键退出。")


def _list_current_file(root_dir: str, dir_list: list[str]):
    current_files: list[str] = ["语言文件修改文件列表：", "被修改的文件：" + root_dir, "应用修改的文件："]
    for i in range(len(dir_list)):
        current_files.append(str(i + 1) + ". " + dir_list[i])
    for s in current_files:
        print(s)


def _notify_modification(msgid: str, old_str: str, new_str: str):
    print("")
    print(splitter_str)
    print(f"修改“{msgid}”键：")
    print(old_str)
    print(">>>")
    print(new_str)
    print(splitter_str)
    print("")


def _notify_modification_plural(msgid: str, old_strs: list[str], new_strs: list[str]):
    print("")
    print(splitter_str)
    print(f"修改“{msgid}”键：")
    for o in old_strs:
        print(o)
    print(">>>")
    for n in new_strs:
        print(n)
    print(splitter_str)
    print("")


def _process_modification_file(source_po, translated_path: str):
    if translated_path.endswith("po"):
        translated = polib.pofile(translated_path)
    else:
        translated = polib.mofile(translated_path)
    translation_dict_singular = {entry.msgid: entry.msgstr for entry in translated}
    translation_dict_plural: dict[str, list[str]] = {entry.msgid_plural: entry.msgstr_plural for entry in
                                                     translated}
    singular_empty = len(translation_dict_singular) == 0
    plural_empty = len(translation_dict_plural) == 0
    for entry in source_po:
        if not singular_empty and entry.msgid and entry.msgid in translation_dict_singular:
            old_str = entry.msgstr
            entry.msgstr = translation_dict_singular[entry.msgid]
            _notify_modification(entry.msgid, old_str, entry.msgstr)
            del translation_dict_singular[entry.msgid]
            singular_empty = len(translation_dict_singular) == 0
        if not plural_empty and entry.msgid_plural and entry.msgid_plural in translation_dict_plural:
            old_strs = entry.msgstr_plural.copy()
            entry.msgstr_plural = translation_dict_plural.get(entry.msgid_plural)
            _notify_modification_plural(entry.msgstr_plural, old_strs, entry.msgstr_plural)
            del translation_dict_plural[entry.msgid_plural]
            plural_empty = len(translation_dict_plural) == 0


try:
    run()
except Exception as e:
    feedback = input(f"发生异常！异常信息：{e}。")
