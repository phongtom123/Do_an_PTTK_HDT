class Lesson:
    def __init__(self, lesson_ID, unit_ID, lessonName):
        self.lesson_ID = lesson_ID
        self.unit_ID = unit_ID
        self.lessonName = lessonName

    def get_lessonName(self):
        return self.lessonName

class Reading(Lesson):
    def __init__(self, lesson_ID, unit_ID, lessonName, readContent):
        super().__init__(lesson_ID, unit_ID, lessonName)
        self.readContent = readContent

class Listening(Lesson):
    def __init__(self, lesson_ID, unit_ID, lessonName, linkAudio):
        super().__init__(lesson_ID, unit_ID, lessonName)
        self.linkAudio = linkAudio
