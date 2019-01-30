from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible import errors
from ansible.utils.display import Display

display = Display()


class TestModule(object):

    def tests(self):
        return {'file_mode': self.do_file_mode}

    def do_file_mode(self, a, mask):

        if not all(d.isdigit() and int(d) < 8 for d in a) or len(a) > 4:
            raise errors.AnsibleFilterError("file_mode requires a file mode input, got %s instead." % a)

        if not all(mask.isdigit() and int(d) < 8 for d in a) or len(mask) > 4:
            raise errors.AnsibleFilterError("file_mode requires a file mode mask, got %s instead." % a)

        return all(int(x) & ~int(y) is 0 for x, y in zip(a.zfill(4), mask.zfill(4)))


def test_mode():
    assert TestModule().do_file_mode('0400', '7740')
    assert TestModule().do_file_mode('0600', '7740')
    assert TestModule().do_file_mode('0640', '7740')
    assert not TestModule().do_file_mode('0777', '7740')
    assert not TestModule().do_file_mode('0764', '7740')
