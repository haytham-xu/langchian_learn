
from dotenv import load_dotenv
load_dotenv(".secret/.env")

from langchain.text_splitter import Language
from langchain_community.document_loaders.generic import GenericLoader
from langchain_community.document_loaders.parsers import LanguageParser
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationSummaryMemory
from langchain_openai import ChatOpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

import re
import subprocess

# -----------utils----------------

def run_maven_test_in_directory(directory):
    command = ["mvn", "test"]
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=directory)
    stdout, stderr = process.communicate()
    stdout = stdout.decode().strip()
    stderr = stderr.decode().strip()
    return stdout, stderr

def write_list_to_file(file_path, str_list):
    with open(file_path, 'w') as f:
        for item in str_list:
            f.write("%s\n" % item)

def extract_text(content):
    matches = re.findall(r'```(?:java|python|js)\n(.*?)```', content, re.DOTALL)
    lines = [line for match in matches for line in match.split('\n') if line.strip()]
    return lines

def write_and_execute_ut(ut_code):
    write_list_to_file(ut_output_path, ut_code)
    _, stderr = run_maven_test_in_directory(ut_root_path)
    return stderr

def display(text):
    print()
    print()
    print(text)
    print()
    print()
    

# -----------main----------------

repo_path = "/Users/i353667/Documents/code/github.com/book-management-system"
ut_root_path = "/Users/i353667/Documents/code/github.com/book-management-system/src/test/java/com/haythamxu/controller"
ut_output_path = ut_root_path + "/BookControllerIntegrationTest.java"
directory = "/Users/i353667/Documents/code/github.com/book-management-system"
question = "give me integration test Java code for BookController, only code, don't append other message."

# Load
loader = GenericLoader.from_filesystem(
    repo_path,
    glob="**/*",
    suffixes=[".java"],
    exclude=["**/target/**"],
    parser=LanguageParser(language=Language.JAVA, parser_threshold=500),
)
documents = loader.load()

python_splitter = RecursiveCharacterTextSplitter.from_language(
    language=Language.JAVA, chunk_size=2000, chunk_overlap=200
)
texts = python_splitter.split_documents(documents)

db = Chroma.from_documents(texts, OpenAIEmbeddings(disallowed_special=()))
retriever = db.as_retriever(
    search_type="mmr",  # Also test "similarity"
    search_kwargs={"k": 8},
)

llm = ChatOpenAI(model_name="gpt-3.5-turbo")
memory = ConversationSummaryMemory(
    llm=llm, memory_key="chat_history", return_messages=True
)
qa = ConversationalRetrievalChain.from_llm(llm, retriever=retriever, memory=memory)

def ut_writer():
    loop_amount=0
    message = question
    while True:
        if loop_amount > 2:
            break
        loop_amount += 1
        display("message: " + message)
        result = qa.invoke(message)
        res = result["answer"]
        display("result: " + res)
        res = extract_text(res)
        stderr = write_and_execute_ut(res)
        display("stderr: " + stderr)
        if stderr == "":
            break
        message = stderr
ut_writer()
# res.insert(0, libraries)


# 使用示例
# stdout, stderr = run_maven_test_in_directory(directory)

# print(stderr)
# print(stderr == "")







# ----------test data----------
# libraries = '''
# package com.haythamxu.controller;

# import com.haythamxu.dto.BookDTO;
# import com.haythamxu.entity.Book;
# import com.haythamxu.service.BookService;
# import org.junit.jupiter.api.Test;
# import org.junit.runner.RunWith;
# import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
# import org.springframework.boot.test.context.SpringBootTest;
# import org.springframework.boot.test.mock.mockito.MockBean;
# import org.springframework.test.context.junit4.SpringRunner;
# import org.springframework.beans.factory.annotation.Autowired;
# import org.springframework.http.MediaType;
# import org.springframework.test.web.servlet.MockMvc;
# import com.fasterxml.jackson.databind.ObjectMapper;
# import static org.mockito.Mockito.*;
# import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.*;
# import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;
# import static org.hamcrest.Matchers.is;

# import java.util.ArrayList;
# import java.util.List;
# '''

# res = '''
# 'The integration test Java code for BookController would typically involve using a testing framework like JUnit and mocking dependencies using tools like Mockito. Here\'s an example of how the integration test code for BookController might look like:
# ```java
# @RunWith(SpringRunner.class)
# @SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
# @AutoConfigureMockMvc
# public class BookControllerIntegrationTest {
#     @Autowired
#     private MockMvc mockMvc;
#     @MockBean
#     private BookService bookService;
#     @Autowired
#     private ObjectMapper objectMapper;
#     @Test
#     public void testAddBook() throws Exception {
#         // Create a BookDTO object with test data
#         BookDTO bookDTO = new BookDTO();
#         bookDTO.setTitle("Test Book");
#         bookDTO.setAuthor("Test Author");
#         bookDTO.setIsbn("1234567890");
#         bookDTO.setPublisher("Test Publisher");
#         // Convert the BookDTO object to JSON
#         String json = objectMapper.writeValueAsString(bookDTO);
#         // Mock the behavior of the bookService
#         when(bookService.getBookByIsbn(anyString())).thenReturn(null);
#         // Perform the POST request to add a book
#         mockMvc.perform(post("/book")
#                 .contentType(MediaType.APPLICATION_JSON)
#                 .content(json))
#                 .andExpect(status().isOk())
#                 .andExpect(content().string("New Book added."));
#         // Verify that the bookService method was called
#         verify(bookService, times(1)).addBook(any(Book.class));
#     }
#     @Test
#     public void testSearchBooks() throws Exception {
#         // Create a Book object with test data
#         Book book = new Book();
#         book.setTitle("Test Book");
#         book.setAuthor("Test Author");
#         book.setIsbn("1234567890");
#         book.setPublisher("Test Publisher");
#         // Mock the behavior of the bookService
#         when(bookService.getBookByIsbn("1234567890")).thenReturn(book);
#         // Perform the GET request to search for a book
#         mockMvc.perform(get("/search/1234567890"))
#                 .andExpect(status().isOk())
#                 .andExpect(jsonPath("$.title", is("Test Book")))
#                 .andExpect(jsonPath("$.author", is("Test Author")))
#                 .andExpect(jsonPath("$.isbn", is("1234567890")))
#                 .andExpect(jsonPath("$.publisher", is("Test Publisher")));
#     }
#     @Test
#     public void testGetAllBooks() throws Exception {
#         // Create a list of Book objects with test data
#         List<Book> books = new ArrayList<>();
#         Book book1 = new Book();
#         book1.setTitle("Test Book 1");
#         book1.setAuthor("Test Author 1");
#         book1.setIsbn("1234567890");
#         book1.setPublisher("Test Publisher 1");
#         books.add(book1);
#         Book book2 = new Book();
#         book2.setTitle("Test Book 2");
#         book2.setAuthor("Test Author 2");
#         book2.setIsbn("0987654321");
#         book2.setPublisher("Test Publisher 2");
#         books.add(book2);
#         // Mock the behavior of the bookService
#         when(bookService.getAllBooks()).thenReturn(books);
#         // Perform the GET request to get all books
#         mockMvc.perform(get("/search"))
#                 .andExpect(status().isOk())
#                 .andExpect(jsonPath("$[0].title", is("Test Book 1")))
#                 .andExpect(jsonPath("$[0].author", is("Test Author 1")))
#                 .andExpect(jsonPath("$[0].isbn", is("1234567890")))
#                 .andExpect(jsonPath("$[0].publisher", is("Test Publisher 1")))
#                 .andExpect(jsonPath("$[1].title", is("Test Book 2")))
#                 .andExpect(jsonPath("$[1].author", is("Test Author 2")))
#                 .andExpect(jsonPath("$[1].isbn", is("0987654321")))
#                 .andExpect(jsonPath("$[1].publisher", is("Test Publisher 2")));
#     }
# }
# ```
# ksuhefjahbr
# '''