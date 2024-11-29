import time
import threading
import cv2
import numpy as np
import mss
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def record_screen(filename="test_recording.mp4", duration=15):
    with mss.mss() as sct:
        monitor = sct.monitors[1]
        width, height = monitor["width"], monitor["height"]

        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        out = cv2.VideoWriter(filename, fourcc, 10.0, (width, height))

        start_time = time.time()
        while True:
            img = np.array(sct.grab(monitor))
            frame = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
            out.write(frame)

            if time.time() - start_time > duration:
                break

        out.release()

@pytest.fixture(scope="module")
def driver():
    browser = webdriver.Chrome()
    browser.get("https://tdd-detroid.onrender.com/")
    duration = 15
    record_thread = threading.Thread(target=record_screen, args=("records/test_recording.mp4", duration))
    record_thread.start()
    yield browser
    browser.quit()
    record_thread.join()

def test_add_student(driver: WebDriver):
    student_name = "Robson"
    driver.find_element(By.ID, "student-nome").send_keys(student_name)
    WebDriverWait(driver, 10).until(
    EC.invisibility_of_element((By.ID, "pyscript_loading_splash"))) 
    driver.find_element(By.ID, "student-btn").click()
    terminal_output = driver.find_element(By.XPATH, '//div[@id="local-terminal"]/pre').text
    assert student_name in terminal_output, f"Student '{student_name}' not added."

def test_add_course_portuguese(driver: WebDriver):
    course_name = "Portuguese"
    driver.find_element(By.ID, "course-nome").send_keys(course_name)
    driver.find_element(By.ID, "course-btn").click()
    terminal_output = driver.find_element(By.XPATH, '//div[@id="local-terminal"]/pre').text
    assert course_name in terminal_output, f"Course '{course_name}' not added."

def test_add_course_history(driver: WebDriver):
    course_name = "History"
    driver.find_element(By.ID, "course-nome").send_keys(Keys.CONTROL + "a")
    driver.find_element(By.ID, "course-nome").send_keys(Keys.SPACE)
    driver.find_element(By.ID, "course-nome").send_keys(course_name)
    driver.find_element(By.ID, "course-btn").click()
    terminal_output = driver.find_element(By.XPATH, '//div[@id="local-terminal"]/pre').text
    assert course_name in terminal_output, f"Course '{course_name}' not added."

def test_add_course_math(driver: WebDriver):
    course_name = "Math"
    driver.find_element(By.ID, "course-nome").send_keys(Keys.CONTROL + "a")
    driver.find_element(By.ID, "course-nome").send_keys(Keys.SPACE)
    driver.find_element(By.ID, "course-nome").send_keys(course_name)
    driver.find_element(By.ID, "course-btn").click()
    terminal_output = driver.find_element(By.XPATH, '//div[@id="local-terminal"]/pre').text
    assert course_name in terminal_output, f"Course '{course_name}' not added."

def test_add_discipline_grammar(driver: WebDriver):
    discipline_name = "Grammar"
    course_id = "1"
    driver.find_element(By.ID, "discipline-nome").send_keys(discipline_name)
    driver.find_element(By.ID, "course-discipline-id").send_keys(course_id)
    driver.find_element(By.XPATH, '//button[@py-click="add_discipline()"]').click()
    terminal_output = driver.find_element(By.XPATH, '//div[@id="local-terminal"]/pre').text
    assert discipline_name in terminal_output, f"Discipline '{discipline_name}' not added."

def test_add_discipline_linguistics(driver: WebDriver):
    discipline_name = "Linguistics"
    driver.find_element(By.ID, "discipline-nome").send_keys(Keys.CONTROL + "a")
    driver.find_element(By.ID, "discipline-nome").send_keys(Keys.SPACE)
    driver.find_element(By.ID, "discipline-nome").send_keys(discipline_name)
    driver.find_element(By.XPATH, '//button[@py-click="add_discipline()"]').click()
    terminal_output = driver.find_element(By.XPATH, '//div[@id="local-terminal"]/pre').text
    assert discipline_name in terminal_output, f"Discipline '{discipline_name}' not added."

def test_add_discipline_essays(driver: WebDriver):
    discipline_name = "Essays"
    driver.find_element(By.ID, "discipline-nome").send_keys(Keys.CONTROL + "a")
    driver.find_element(By.ID, "discipline-nome").send_keys(Keys.SPACE)
    driver.find_element(By.ID, "discipline-nome").send_keys(discipline_name)
    driver.find_element(By.XPATH, '//button[@py-click="add_discipline()"]').click()
    terminal_output = driver.find_element(By.XPATH, '//div[@id="local-terminal"]/pre').text
    assert discipline_name in terminal_output, f"Discipline '{discipline_name}' not added."    

def test_enroll_student_in_course(driver: WebDriver):
    student_id = "1"
    course_id = "1"
    driver.find_element(By.ID, "student-id").send_keys(student_id)
    driver.find_element(By.ID, "course-id").send_keys(course_id)
    driver.find_element(By.XPATH, '//button[@py-click="subscribe_course()"]').click()
    terminal_output = driver.find_element(By.XPATH, '//div[@id="local-terminal"]/pre').text
    assert f"Student id {student_id}" in terminal_output and f"course id {course_id}" in terminal_output, \
        f"Student {student_id} not enrolled in course {course_id}."

def test_enroll_student_in_discipline_1(driver: WebDriver):
    student_name = "Robson"
    student_id = "1"
    discipline_id = "1"
    driver.find_element(By.ID, "subscribe-student-id").send_keys(student_id)
    driver.find_element(By.ID, "subscribe-discipline-id").send_keys(discipline_id)
    driver.find_element(By.XPATH, '//button[@py-click="subscribe_discipline()"]').click()
    terminal_output = driver.find_element(By.XPATH, '//div[@id="local-terminal"]/pre[2]').text
    assert f"Student id {student_id}" in terminal_output and f"{student_name}" in terminal_output and f"discipline id {discipline_id}" in terminal_output, \
        f"Student {student_id} not enrolled in discipline {discipline_id}."
    
def test_enroll_student_in_discipline_2(driver: WebDriver):
    student_name = "Robson"
    student_id = "1"
    discipline_id = "2"
    driver.find_element(By.ID, "subscribe-discipline-id").send_keys(Keys.CONTROL + "a")
    driver.find_element(By.ID, "subscribe-discipline-id").send_keys(Keys.SPACE)
    driver.find_element(By.ID, "subscribe-discipline-id").send_keys(discipline_id)
    driver.find_element(By.XPATH, '//button[@py-click="subscribe_discipline()"]').click()
    terminal_output = driver.find_element(By.XPATH, '//div[@id="local-terminal"]/pre[2]').text
    assert f"Student id {student_id}" in terminal_output and f"{student_name}" in terminal_output and f"discipline id {discipline_id}" in terminal_output, \
        f"Student {student_id} not enrolled in discipline {discipline_id}."
    
def test_enroll_student_in_discipline_3(driver: WebDriver):
    student_name = "Robson"
    student_id = "1"
    discipline_id = "3"
    driver.find_element(By.ID, "subscribe-discipline-id").send_keys(Keys.CONTROL + "a")
    driver.find_element(By.ID, "subscribe-discipline-id").send_keys(Keys.SPACE)
    driver.find_element(By.ID, "subscribe-discipline-id").send_keys(discipline_id)
    driver.find_element(By.XPATH, '//button[@py-click="subscribe_discipline()"]').click()
    terminal_output = driver.find_element(By.XPATH, '//div[@id="local-terminal"]/pre').text
    assert f"Student id {student_id}" in terminal_output and f"{student_name}" in terminal_output and f"discipline id {discipline_id}" in terminal_output, \
        f"Student {student_id} not enrolled in discipline {discipline_id}."

