
#### LangChain Library
* langchain_openai
    * ChatOpenAI: 一个封装了LLM的函数，实体可以
        * (model="gpt-3.5-turbo", temperature=0)
    * OpenAI
        * (model="gpt-3.5-turbo", temperature=0)
    * OpenAIEmbeddings
* langchain.schema
    * HumanMessage: 用于标识自然人输入的消息信息
    * SystemMessage： 用于标识系统的信息，比如设置prompt的告知LLM的role等
    * AIMessage： LLM返回的信息
* langchain.memory
    * ConversationBufferMemory：以原文形式存储记忆信息
        * ()
        * chat_memory.add_user_message：添加自然心输入信息
        * chat_memory.add_ai_message：添加AI返回信息
        * load_memory_variables({})：获取存储记忆信息
    * ConversationBufferWindowMemory：以原文形存储记忆信息，
        * (k)：可设置队列长度k
        * save_context({"input": ""}, {"output": ""})：一次性写入自然人和AI的聊天信息
        * load_memory_variables({})：获取存储记忆信息
    * ConversationSummaryMemory：存储经过AI总结之后的记忆信息，节省token，适用于长上下文沟通, 因为需要LLM总结所以需要发起网络请求
        * (llm=llm, max_token_limit=10)： 可设置token长度
        * save_context({"input": "hi"}, {"output": "whats up"})：一次性写入自然人和AI的聊天信息
        * load_memory_variables({})：获取存储记忆信息
* langchain.chains
    * LLMChain(llm=llm, prompt=prompt, verbose=True, memory=memory)：可以接收LLM, prompt, memory等，构造完后是执行的入口
    * ConversationChain： 接收一个LLM如ChatOpenAI， 内建Memory，可以持续的进行带上下文的聊天
    * ConversationalRetrievalChain
* langchain.prompts
    * ChatPromptTemplate：用于定义Prompts的模板，包内下面三个属性字段
    * SystemMessagePromptTemplate: 类似SystemMessage： 用于标识系统的信息，比如设置prompt的告知LLM的role等
    * MessagesPlaceholder(variable_name="chat_history")：用于Memory的标识，variable_name名称应该保持和Memory内的一致
    * HumanMessagePromptTemplate：类似HumanMessage: 用于标识自然人输入的消息信息，用于接收认为输入信息的模板，一般是占位符
* langchain_community.document_loaders
    * WebBaseLoader
* langchain_community.vectorstores
    * Chroma
* langchain.text_splitter
    * RecursiveCharacterTextSplitter
    

#### 
* LLM
* Memory
* Loader --> TextSplitter --> VectorStores --> Retriever --> Chain 


