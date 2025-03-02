from rag_manager.manager import RAGManager

def main():
    manager = RAGManager()
    while True:
        print("\nMenu:")
        print("1. List all domains")
        print("2. Add a new domain")
        print("3. Load a domain")
        print("4. Generate a prompt")
        print("5. Add data to a domain")
        print("6. Perform text search")
        print("7. Perform embedding search")
        print("8. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            domains = manager.list_domains()
            for domain in domains:
                print(f"Domain: {domain['domain']}, Model: {domain['model']}")
        elif choice == '2':
            domain_name = input("Enter domain name: ")
            model_name = input("Enter model name: ")
            manager.add_domain(domain_name, model_name)
            print(f"Domain {domain_name} with model {model_name} added.")
        elif choice == '3':
            domain_name = input("Enter domain name: ")
            model_name = input("Enter model name: ")
            manager.load_domain(domain_name, model_name)
            print(f"Domain {domain_name} with model {model_name} loaded.")
        elif choice == '4':
            domain_name = input("Enter domain name: ")
            model_name = input("Enter model name: ")
            query = input("Enter query: ")
            mode = input("Enter mode (text/embedding/hybrid): ")
            prompt = manager.generate_prompt(domain_name, model_name, query, mode)
            print(f"Generated prompt: {prompt}")
        elif choice == '5':
            domain_name = input("Enter domain name: ")
            model_name = input("Enter model name: ")
            document = input("Enter document data: ")
            manager.add_data(domain_name, model_name, {"data": document})
            print(f"Data added to domain {domain_name} with model {model_name}.")
        elif choice == '6':
            domain_name = input("Enter domain name: ")
            model_name = input("Enter model name: ")
            query = input("Enter query: ")
            results = manager.generate_prompt(domain_name, model_name, query, "text")
            print(f"Text search results: {results}")
        elif choice == '7':
            domain_name = input("Enter domain name: ")
            model_name = input("Enter model name: ")
            query = input("Enter query: ")
            results = manager.generate_prompt(domain_name, model_name, query, "embedding")
            print(f"Hybrid search results: {results}")
        elif choice == '8':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
