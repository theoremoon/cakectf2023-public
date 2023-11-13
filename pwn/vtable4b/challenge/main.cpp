#include <csignal>
#include <iostream>
#include <iomanip>
#include <fcntl.h>
#include <unistd.h>

void *valid_vtable, *valid_message;

const char *PRIV[] = {
  "---", "--x", "-w-", "-wx", "r--", "r-x", "rw-", "rwx"
};
int get_privilege(void *addr) {
  int priv = 0;
  unsigned long start, end, target;
  char buf[0x100], *ptr;
  int fd = open("/proc/self/maps", O_RDONLY);
  target = (unsigned long)addr;
  for(ptr = buf, start = end = 0; ; ptr++) {
    if (read(fd, ptr, 1) <= 0) {
      break;
    }
    if (*ptr == '-' && start == 0) {
      start = strtol(buf, NULL, 16);
      ptr = buf - 1;
    } else if (*ptr == ' ' && end == 0) {
      end = strtol(buf, NULL, 16);
      ptr = buf - 1;
    } else if (*ptr == '\n') {
      if (start <= target && target < end) {
        priv |= (buf[0] == 'r') << 2;
        priv |= (buf[1] == 'w') << 1;
        priv |= (buf[2] == 'x') << 0;
        break;
      }
      start = end = 0;
      ptr = buf - 1;
    }
  }
  
  close(fd);
  return priv;
}

static void win() {
  char *args[] = {"/bin/sh", NULL};
  std::cout << "[+] Congratulations! Executing shell..." << std::endl
            << "$ ";
  execve(args[0], args, NULL);
  std::cout << "[-] Failed to execute shell :thinking_face:" << std::endl;
}

class Cowsay {
public:
  Cowsay(char *message) : message_(message) {}
  char*& message() { return message_; }
  virtual void dialogue();

private:
  char *message_;
};

void Cowsay::dialogue() {;
  std::cout << " _______________________ "       << std::endl
            << "< " << std::left << std::setfill(' ') << std::setw(21)
            << message_ << " >" << std::endl
            << " -----------------------"        << std::endl
            << "        \\   ^__^"               << std::endl
            << "         \\  (oo)\\_______"      << std::endl
            << "            (__)\\       )\\/\\" << std::endl
            << "                ||----w |"       << std::endl
            << "                ||     ||\n"     << std::endl;
}

void display_heap(Cowsay *cowsay) {
  int draw_vtable = 0;
  void *vtable;
  size_t p = (size_t)valid_message - 0x10;
  std::cout << std::endl << std::right
            << "  [ address ]    [ heap data ]" << std::endl
            << "               +------------------+" << std::endl;

  for (int i = 0; i < 10; i++, p += 8) {
    std::cout << "0x" << std::setfill('0') << std::setw(12) << std::hex << p
              << " | " << std::setw(16) << std::hex << *(size_t*)p << " |";

    if (draw_vtable == 1) {
      std::cout << "  0x" << std::setw(12) << (size_t)vtable
                << " | " << std::setw(16)
                << *((size_t*)vtable + draw_vtable - 1) << " |";
      draw_vtable++;
    } else if (draw_vtable == 2) {
      size_t fn = *(size_t*)vtable;
      if (fn == *(size_t*)valid_vtable) {
        std::cout << "                 --> Cowsay::dialogue";
      } else if (fn == (size_t)&win) {
        std::cout << "                 --> <win> function";
      } else if (get_privilege((void*)fn) & 1) {
        std::cout << "                 --> Maybe function pointer";
      } else {
        std::cout << "                 --> Invalid function pointer";
      }
      draw_vtable = 0;
    }

    if (p == (size_t)cowsay) {
      vtable = (void*)(*(size_t*)cowsay);
      if (vtable == valid_vtable) {
        std::cout << " ---------------> vtable for Cowsay";
        draw_vtable = 1;
      } else if (get_privilege(vtable) & 4) {
        std::cout << " ---------------> vtable for Cowsay (corrupted)";
        draw_vtable = 1;
      } else {
        std::cout << " --> Broken vtable pointer";
      }
    } else if (p == (size_t)cowsay->message()) {
      if (get_privilege(cowsay->message()) & 4) {
        std::cout << " <-- message (= '" << cowsay->message() << "')";
      } else {
        std::cout << " <-- message (= invalid pointer)";
      }
    }

    std::cout << std::endl;
    if (draw_vtable) {
      std::cout << "               +------------------+"
                << "                 +------------------+" << std::endl;
    } else {
      std::cout << "               +------------------+" << std::endl;
    }
  }

  std::cout << std::endl;
}

void sigsegv_handler(int signal) {
  std::cout << "[-] Segmentation fault" << std::endl;
  exit(1);
}

int menu() {
  int choice;
  std::cout << "1. Use cowsay" << std::endl
            << "2. Change message" << std::endl
            << "3. Display heap" << std::endl
            << "> ";
  std::cin >> choice;
  return choice;
}

int main() {
  std::setvbuf(stdin, NULL, _IONBF, 0);
  std::setvbuf(stdout, NULL, _IONBF, 0);
  std::signal(SIGSEGV, sigsegv_handler);

  std::cout << "Today, let's learn how to exploit C++ vtable!"   << std::endl
            <<  "You're going to abuse the following C++ class:" << std::endl
            << std::endl
            << "  class Cowsay {"                    << std::endl
            << "  public:"                           << std::endl
            << "    Cowsay(char *message) : message_(message) {}" << std::endl
            << "    char*& message() { return message_; }"        << std::endl
            << "    virtual void dialogue();"        << std::endl << std::endl
            << "  private:"                          << std::endl
            << "    char *message_;"                 << std::endl
            << "  };"                                << std::endl
            << std::endl
            << "An instance of this class is allocated in the heap:"
            << std::endl << std::endl
            << "  Cowsay *cowsay = new Cowsay(new char[0x18]());"
            << std::endl << std::endl
            << "You can" << std::endl
            << " 1. Call `dialogue` method:" << std::endl
            << "  cowsay->dialogue();"       << std::endl
            << std::endl
            << " 2. Set `message`:"               << std::endl
            << "  std::cin >> cowsay->message();" << std::endl
            << std::endl
            << "Last but not least, here is the address of "
    "`win` function which you should call to get the flag:" << std::endl
            << "  <win> = 0x" << std::hex << (size_t)&win
            << std::endl << std::endl;

  Cowsay *cowsay = new Cowsay(new char[0x18]());
  valid_vtable = (void*)(*(size_t*)cowsay);
  valid_message = (void*)cowsay->message();

  while (std::cin.good()) {
    switch(menu()) {
      case 1: {
        std::cout << "[+] You're trying to use vtable at 0x"
                  << std::hex << *(size_t*)cowsay
                  << std::endl;
        cowsay->dialogue();
        break;
      }

      case 2: {
        std::cout << "Message: ";
        std::cin >> cowsay->message();
        break;
      }

      case 3: {
        display_heap(cowsay);
        break;
      }

      default: {
        std::cout << "Bye!" << std::endl;
        return 0;
      }
    }
  }
  return 0;
}
