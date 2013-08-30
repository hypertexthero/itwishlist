"""
DrupalPasswordHasher

To use, put this in any app and add to your settings.py, something like this:

PASSWORD_HASHERS = (
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'myproject.myapp.drupal_hasher.DrupalPasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptPasswordHasher',
    'django.contrib.auth.hashers.SHA1PasswordHasher',
    'django.contrib.auth.hashers.MD5PasswordHasher',
    'django.contrib.auth.hashers.CryptPasswordHasher',
)

Two notes: First, in Drupal the number of iterations is a multiple of 2,
which is represented by the first character after the $, so set the iterations
class member appropriately.

Secondly, in Drupal the passwords are stored as:

$S$<hash>

while in Django the passwords are stored as

S$<hash>

So you must cut off the first character of each password when migrating.
"""





import importlib

class BasePasswordHasher(object):
    """
    Abstract base class for password hashers

    When creating your own hasher, you need to override algorithm,
    verify(), encode() and safe_summary().

    PasswordHasher objects are immutable.
    """
    algorithm = None
    library = None

    def _load_library(self):
        if self.library is not None:
            if isinstance(self.library, (tuple, list)):
                name, mod_path = self.library
            else:
                mod_path = self.library
            try:
                module = importlib.import_module(mod_path)
            except ImportError as e:
                raise ValueError("Couldn't load %r algorithm library: %s" %
                                 (self.__class__.__name__, e))
            return module
        raise ValueError("Hasher %r doesn't specify a library attribute" %
                         self.__class__.__name__)

    def salt(self):
        """
        Generates a cryptographically secure nonce salt in ascii
        """
        return get_random_string()

    def verify(self, password, encoded):
        """
        Checks if the given password is correct
        """
        raise NotImplementedError()

    def encode(self, password, salt):
        """
        Creates an encoded database value

        The result is normally formatted as "algorithm$salt$hash" and
        must be fewer than 128 characters.
        """
        raise NotImplementedError()

    def safe_summary(self, encoded):
        """
        Returns a summary of safe values

        The result is a dictionary and will be used where the password field
        must be displayed to construct a safe representation of the password.
        """
        raise NotImplementedError()






import hashlib

# from django.contrib.auth.hashers import BasePasswordHasher

_ITOA64 = './0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'


class DrupalPasswordHasher(BasePasswordHasher):
    algorithm = "S"
    iter_code = 'C'
    salt_length = 8

    def encode(self, password, salt, iter_code=None):
        """The Drupal 7 method of encoding passwords"""
        if iter_code == None:
            iterations = 2 ** _ITOA64.index(self.iter_code)
        else:
            iterations = 2 ** _ITOA64.index(iter_code)
        hash = hashlib.sha512(salt + password).digest()

        for i in range(iterations):
            hash = hashlib.sha512(hash + password).digest()

        l = len(hash)

        output = ''
        i = 0

        while i < l:
            value = ord(hash[i])
            i = i + 1

            output += _ITOA64[value & 0x3f]
            if i < l:
                value |= ord(hash[i]) << 8

            output += _ITOA64[(value >> 6) & 0x3f]
            if i >= l:
                break
            i += 1

            if i < l:
                value |= ord(hash[i]) << 16

            output += _ITOA64[(value >> 12) & 0x3f]
            if i >= l:
                break
            i += 1

            output += _ITOA64[(value >> 18) & 0x3f]

        longhashed = "%s$%s%s%s" % (self.algorithm, iter_code,
                                    salt, output)
        return longhashed[:54]

    def verify(self, password, encoded):
        hash = encoded.split("$")[1]
        iter_code = hash[0]
        salt = hash[1:1 + self.salt_length]
        return encoded == self.encode(password, salt, iter_code)