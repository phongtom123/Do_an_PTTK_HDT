from abc import ABC, abstractmethod

class Test(ABC):
    def __init__(self, test_id, test_content):
        self._test_id = test_id
        self._test_content = test_content

    def get_test_id(self):
        return self._test_id

    def get_test_content(self):
        return self._test_content

    # ====== ABSTRACT METHOD ======
    @abstractmethod
    def get_content(self):
        """Các lớp con bắt buộc phải implement"""
        pass

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self._test_id})"
