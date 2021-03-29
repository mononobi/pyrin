# -*- coding: utf-8 -*-
"""
utils path module.
"""

import os
import sys
import shutil

import pyrin.utils.environment as env_utils

from pyrin.core.globals import _
from pyrin.utils.exceptions import PathIsNotAbsoluteError, InvalidPathError, \
    PathNotExistedError, PathAlreadyExistedError, IsNotDirectoryError, IsNotFileError


def get_module_file_path(module_name):
    """
    gets the absolute file path of module with given name.

    :param str module_name: module name to get its file path.

    :rtype: str
    """

    return os.path.abspath(sys.modules[module_name].__file__)


def get_main_package_name(module_name):
    """
    gets the main package name from given module name.

    for example for `pyrin.database.manager` module, it
    returns `pyrin` as the main package name.

    :param str module_name: module name to get its root package name.

    :rtype: str
    """

    return module_name.split('.')[0]


def get_main_package_path(module_name):
    """
    gets the absolute path of the main package of module with given name.

    :param str module_name: module name to get its main package path.

    :rtype: str
    """

    relative_module_path = module_name.replace('.', os.path.sep)
    root_package = get_main_package_name(module_name)
    absolute_module_path = get_module_file_path(module_name)
    temp_absolute_module_path = absolute_module_path.replace(relative_module_path, '*')
    excess_part = temp_absolute_module_path.split('*')[-1]
    list_path = list(temp_absolute_module_path)

    for i in range(-1, -len(list_path), -1):
        if list_path[i] == '*':
            list_path[i] = root_package
            break

    main_package_path = ''.join(list_path)
    main_package_path = main_package_path.replace('*', relative_module_path)
    main_package_path = main_package_path.replace(excess_part, '').rstrip(os.path.sep)

    return main_package_path


def get_pyrin_main_package_name():
    """
    gets the name of pyrin main package name.

    it would always be `pyrin` in normal cases.

    :rtype: str
    """

    return get_main_package_name(__name__)


def get_pyrin_main_package_path():
    """
    gets the absolute path of pyrin main package.

    :rtype: str
    """

    return get_main_package_path(__name__)


def get_package_name(path, root_path):
    """
    gets the full package name for provided path.

    :param str path: full path of package.
                     example path = `/home/src/pyrin/database`.

    :param str root_path: root path in which this path is located.
                          example root_path = `/home/src`

    :rtype: str
    """

    return path.replace(root_path, '').replace(os.path.sep, '.').lstrip('.')


def get_package_path(module_name):
    """
    gets the absolute path of the package of module with given name.

    :param str module_name: module name to get its package path.

    :rtype: str
    """

    absolute_module_path = get_module_file_path(module_name)
    parts = os.path.split(absolute_module_path)
    return parts[0]


def create_directory(target, ignore_existed=False):
    """
    creates a directory with given absolute target path.

    it will create all not available intermediate directories as well.

    :param str target: absolute path of directory to be created.

    :param bool ignore_existed: specifies that if the directory is
                                already existed, ignore it. otherwise
                                raise an error. defaults to False

    :raises InvalidPathError: invalid path error.
    :raises PathIsNotAbsoluteError: path is not absolute error.
    :raises PathAlreadyExistedError: path already existed error.
    """

    if ignore_existed is not True:
        assert_not_exists(target)

    os.makedirs(target, exist_ok=ignore_existed)


def copy_file(source, target):
    """
    copies the given source file into given target file or directory.

    note that target could also be a directory, if so,
    then the file with the source name will be generated.
    both source and target paths must be absolute.

    :param str source: source file absolute path.
    :param str target: target file or directory absolute path.

    :raises InvalidPathError: invalid path error.
    :raises PathIsNotAbsoluteError: path is not absolute error.
    :raises PathNotExistedError: path not existed error.
    """

    assert_exists(source)
    assert_absolute(target)
    shutil.copy2(source, target)


def remove_file(source):
    """
    removes the given source file.

    :param str source: source file absolute path.

    :raises InvalidPathError: invalid path error.
    :raises PathIsNotAbsoluteError: path is not absolute error.
    :raises PathNotExistedError: path not existed error.
    """

    assert_exists(source)
    os.remove(source)


def copy_directory(source, target, ignore_existed=False, ignore=None):
    """
    copies the given source directory contents into given target directory.

    both source and target paths must be absolute.

    :param str source: source directory absolute path.
    :param str target: target directory absolute path.

    :param bool ignore_existed: specifies that if the destination directory
                                is already existed, it should not raise an error.
                                defaults to False if not provided.

    :param callable ignore: the optional ignore argument is a callable. if given, it
                            is called with the `source` parameter, which is the directory
                            being visited by copytree(), and `names` which is the list of
                            `source` contents, as returned by os.listdir():
                            callable(src, names) -> ignored_names

    :raises InvalidPathError: invalid path error.
    :raises PathIsNotAbsoluteError: path is not absolute error.
    :raises PathNotExistedError: path not existed error.
    """

    assert_exists(source)
    assert_absolute(target)
    copytree_ex(source, target, ignore=ignore, ignore_existed=ignore_existed)


def assert_absolute(source):
    """
    asserts that given source path is absolute.

    :param str source: source path to be checked.

    :raises InvalidPathError: invalid path error.
    :raises PathIsNotAbsoluteError: path is not absolute error.
    """

    if source is None:
        raise InvalidPathError(_('Provided path could not be None.'))

    if not os.path.isabs(source):
        raise PathIsNotAbsoluteError(_('Provided path [{source}] must be absolute.')
                                     .format(source=source))


def exists(source):
    """
    gets a value indicating that given source path exists on file system.

    :param str source: source path to be checked for existence.
                       it must be an absolute path.

    :raises InvalidPathError: invalid path error.
    :raises PathIsNotAbsoluteError: path is not absolute error.
    """

    assert_absolute(source)
    return os.path.exists(source)


def assert_exists(source):
    """
    asserts that given source path exists on file system.

    :param str source: source path to be checked for existence.
                       it must be an absolute path.

    :raises InvalidPathError: invalid path error.
    :raises PathIsNotAbsoluteError: path is not absolute error.
    :raises PathNotExistedError: path not existed error.
    """

    if not exists(source):
        raise PathNotExistedError(_('Provided path [{source}] does not exist.')
                                  .format(source=source))


def assert_not_exists(source):
    """
    asserts that given source path not exists on file system.

    :param str source: source path to be checked for not existence.
                       it must be an absolute path.

    :raises InvalidPathError: invalid path error.
    :raises PathIsNotAbsoluteError: path is not absolute error.
    :raises PathAlreadyExistedError: path already existed error.
    """

    if exists(source):
        raise PathAlreadyExistedError(_('Provided path [{source}] already existed.')
                                      .format(source=source))


def get_first_available_file(*paths, file_name):
    """
    gets the first path which a file with given name is resided in it.

    it returns None if the file is not available in any of given paths.

    :param str paths: paths to look for file in them.
                      all paths must be absolute.

    :param str file_name: file name with extension to look for.

    :raises InvalidPathError: invalid path error.
    :raises PathIsNotAbsoluteError: path is not absolute error.

    :rtype: str
    """

    for single_path in paths:
        assert_absolute(single_path)
        file_path = os.path.abspath(os.path.join(single_path, file_name))
        if os.path.isfile(file_path):
            return file_path

    return None


def copytree_ex(source, destination, symlinks=False, ignore=None,
                copy_function=shutil.copy2, ignore_dangling_symlinks=False,
                ignore_existed=False):
    """
    recursively copy a directory tree.

    this method patches the `shutil.copytree()` method to let the caller decide
    to let or not to let to copy if destination directory is already existed.
    if exception(s) occur, an error is raised with a list of reasons.

    :param str source: source directory.
    :param str destination: destination directory.

    :param bool symlinks: if the optional symlinks flag is True, symbolic links in the
                          source tree result in symbolic links in the destination tree.
                          if it is false, the contents of the files pointed to by symbolic
                          links are copied. if the file pointed by the symlink doesn't
                          exist, an exception will be added in the list of errors raised in
                          an error exception at the end of the copy process. defaults to
                          False if not provided.

    :param callable ignore: the optional ignore argument is a callable. if given, it
                            is called with the `source` parameter, which is the directory
                            being visited by copytree(), and `names` which is the list of
                            `source` contents, as returned by os.listdir():
                            callable(src, names) -> ignored_names

    :param callable copy_function: is a callable that will be used to copy each file.
                                   it will be called with the source path and the
                                   destination path as arguments. by default, `copy2()`
                                   is used, but any function that supports the same
                                   signature can be used.

    :param bool ignore_dangling_symlinks: if set to True, the exception for broken
                                          symlinks will not be raised.
                                          defaults to False if not provided.

    :param bool ignore_existed: specifies that if the destination directory
                                is already existed, it should not raise an error.
                                defaults to False if not provided.
    """

    names = os.listdir(source)
    if ignore is not None:
        ignored_names = ignore(source, names)
    else:
        ignored_names = set()

    os.makedirs(destination, exist_ok=ignore_existed)
    errors = []
    for name in names:
        if name in ignored_names:
            continue
        source_name = os.path.join(source, name)
        real_name = name
        if real_name.endswith('-py'):
            real_name = real_name.replace('-py', '.py')
        destination_name = os.path.join(destination, real_name)
        try:
            if os.path.islink(source_name):
                link_to = os.readlink(source_name)
                if symlinks:
                    # We can't just leave it to `copy_function` because legacy
                    # code with a custom `copy_function` may rely on copytree
                    # doing the right thing.
                    os.symlink(link_to, destination_name)
                    shutil.copystat(source_name, destination_name,
                                    follow_symlinks=not symlinks)
                else:
                    # ignore dangling symlink if the flag is on
                    if not os.path.exists(link_to) and ignore_dangling_symlinks:
                        continue
                    # otherwise let the copy occurs. copy2 will raise an error
                    if os.path.isdir(source_name):
                        copytree_ex(source_name, destination_name, symlinks, ignore,
                                    copy_function)
                    else:
                        copy_function(source_name, destination_name)
            elif os.path.isdir(source_name):
                copytree_ex(source_name, destination_name, symlinks, ignore, copy_function)
            else:
                # Will raise a SpecialFileError for unsupported file types
                copy_function(source_name, destination_name)
        # catch the Error from the recursive copytree so that we can
        # continue with other files
        except shutil.Error as err:
            errors.extend(err.args[0])
        except OSError as why:
            errors.append((source_name, destination_name, str(why)))
    try:
        shutil.copystat(source, destination)
    except OSError as why:
        # Copying file access times may fail on Windows
        if getattr(why, 'winerror', None) is None:
            errors.append((source, destination, str(why)))
    if errors:
        raise shutil.Error(errors)


def get_pycache(source, names):
    """
    gets all `__pycache__` directories available in names.

    :param str source: source directory of contents.
    :param list[str] names: name of all contents in source.

    :rtype: list[str]
    """

    return [name for name in names if '__pycache__' in name]


def assert_is_directory(source):
    """
    asserts that given path is a directory.

    :param str source: source path to be checked.
                       it must be an absolute path.

    :raises InvalidPathError: invalid path error.
    :raises PathIsNotAbsoluteError: path is not absolute error.
    :raises PathNotExistedError: path not existed error.
    :raises IsNotDirectoryError: is not directory error.
    """

    assert_exists(source)
    if not os.path.isdir(source):
        raise IsNotDirectoryError(_('Provided path [{source}] is not a directory.')
                                  .format(source=source))


def assert_is_file(source):
    """
    asserts that given path is a file.

    :param str source: source path to be checked.
                       it must be an absolute path.

    :raises InvalidPathError: invalid path error.
    :raises PathIsNotAbsoluteError: path is not absolute error.
    :raises PathNotExistedError: path not existed error.
    :raises IsNotFileError: is not directory error.
    """

    assert_exists(source)
    if not os.path.isfile(source):
        raise IsNotFileError(_('Provided path [{source}] is not a file.')
                             .format(source=source))


def get_file_extension(file, **options):
    """
    gets the extension of given file.

    :param str file: file path to get its extension.

    :keyword bool remove_dot: specifies that the extension must not
                              include the `.` character.
                              defaults to True if not provided.

    :keyword bool lowercase: specifies that extension must be changed to lowercase.
                             defaults to True if not provided.

    :rtype: str
    """

    remove_dot = options.get('remove_dot', True)
    lowercase = options.get('lowercase', True)
    name, extension = os.path.splitext(file)

    if remove_dot is not False:
        extension = extension.replace('.', '')

    if lowercase is not False:
        extension = extension.lower()

    return extension


def get_file_size(file):
    """
    gets the file size in bytes.

    :param str file: file path to get its size.

    :rtype: int
    """

    return os.path.getsize(file)


def get_files(directory, *extensions):
    """
    gets a list of all files in given directory.

    it could filter files with given extensions if provided.
    it only returns files in the root path.

    :param str directory: full path of directory.
    :param str extensions: extension of files to be listed.
                           if not provided, all files will be listed.

    :rtype: list[str]
    """

    extensions = tuple(item.lower() for item in extensions)
    files = []
    for root, directories, file_names in os.walk(directory):
        for item in file_names:
            extension = get_file_extension(item)
            if len(extensions) > 0 and extension not in extensions:
                continue
            full_path = os.path.join(root, item)
            files.append(full_path)
        break

    return files


def get_directories(root):
    """
    gets a list of all directories in given root directory.

    it only returns directories in the root path.

    :param str root: root path.

    :rtype: list[str]
    """

    folders = []
    for root, directories, file_names in os.walk(root):
        for item in directories:
            full_path = os.path.join(root, item)
            folders.append(full_path)
        break

    return folders


def get_last_directory_name(full_path):
    """
    gets the last directory name of given path.

    it returns the exact name of last directory, not the full path.

    :param str full_path: full path of file or directory.

    :rtype: str
    """

    if os.path.isdir(full_path):
        # this is to ensure that path ends with '/'.
        full_path = os.path.join(full_path, '')

    return os.path.basename(os.path.dirname(full_path))


def split_name(full_path):
    """
    gets the root path and the name of the source directory or file.

    :param str full_path: full file or directory path.

    :returns: tuple[str root, str name]
    :rtype: tuple[str, str]
    """

    # this is to ensure that path does not end with '/'.
    full_path = full_path.rstrip(os.path.sep).rstrip(os.path.altsep)
    parts = os.path.split(full_path)
    root = os.path.join(*parts[0:-1])
    return root, parts[-1]


def move(source, destination):
    """
    moves a file or directory from source to destination.

    it returns the new destination path, it may be different from input destination.

    :param str source: source file or directory.
    :param str destination: destination file or directory.

    :rtype: str
    """

    result_path = shutil.move(source, destination)
    if result_path is None:
        result_path = destination

    return result_path


def rename(source, new_name):
    """
    renames the source directory or file to the new name.

    it returns the full path of renamed file or directory.

    :param str source: source file or directory.

    :param str new_name: the new name. it must only be
                         the exact name, not the full path.

    :rtype: str
    """

    root, old_name = split_name(source)
    new_path = os.path.join(root, new_name)
    return move(source, new_path)


def get_file_name(file, **options):
    """
    gets the file name of given file path.

    :param str file: full file path.

    :keyword bool include_extension: specifies that file extension must be included.
                                     defaults to True if not provided.

    :rtype: str
    """

    include_extension = options.get('include_extension', True)
    root, name = split_name(file)

    if include_extension is False:
        extension = get_file_extension(file, remove_dot=False, lowercase=False)
        return name.rstrip(extension)

    return name


def get_directory_name(directory):
    """
    gets the directory name of given directory path.

    :param str directory: full directory path.

    :rtype: str
    """

    # this is to ensure that path ends with '/'.
    directory = os.path.join(directory, '')
    return get_last_directory_name(directory)


def is_same_path(first_path, second_path):
    """
    gets a value indicating that two paths are the same.

    note that it has the correct behavior on case-sensitive
    and case-insensitive operating systems.

    :param str first_path: full first path.
    :param str second_path: full second path.

    :rtype: bool
    """

    if env_utils.is_windows() is True:
        first_path = first_path.lower()
        second_path = second_path.lower()

    return first_path == second_path
