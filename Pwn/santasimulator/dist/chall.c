#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#define MAX_GIFTS 16

typedef struct {
    char sender[8];
    char recipient[8];
    char content[16];
} Gift;

Gift *gifts[MAX_GIFTS];

__attribute__((constructor))
void setup() {
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
}

void menu() {
    puts("");
    puts("[1] Make Gift");
    puts("[2] Check Gift");
    puts("[3] Send Gift");
    puts("[4] Exit");
    printf("> ");
}

long read_int() {
    char buf[32];
    if (fgets(buf, sizeof(buf), stdin) == NULL) {
        exit(1);
    }
    return atol(buf);
}

void make_gift() {
    long idx;
    
    printf("Index: ");
    idx = read_int();
    
    if (idx < 0 || idx >= MAX_GIFTS) {
        puts("Invalid index!");
        return;
    }
    
    if (gifts[idx] != NULL) {
        puts("Slot already in use!");
        return;
    }
    
    gifts[idx] = malloc(sizeof(Gift));
    if (gifts[idx] == NULL) {
        puts("Allocation failed!");
        return;
    }
    
    printf("Sender: ");
    read(0, gifts[idx]->sender, 8);
    
    printf("Recipient: ");
    read(0, gifts[idx]->recipient, 8);
    
    printf("Content: ");
    read(0, gifts[idx]->content, 16);
    
    puts("Created!");
}

void check_gift() {
    long idx;
    
    printf("Index: ");
    idx = read_int();
    
    if (gifts[idx] == NULL) {
        puts("Empty slot!");
        return;
    }
    
    puts("/---------------------------------------\\");
    printf("From: %.8s\n", gifts[idx]->sender);
    printf("To: %.8s\n", gifts[idx]->recipient);
    puts("-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-");
    puts("");
    printf("%.16s\n", gifts[idx]->content);
    puts("");
    puts("\\---------------------------------------/");
}

void send_gift() {
    long idx;
    
    printf("Index: ");
    idx = read_int();
    
    if (gifts[idx] == NULL) {
        puts("Empty slot!");
        return;
    }
    
    free(gifts[idx]);
    gifts[idx] = NULL;
    
    puts("Sent!");
}

int main() {
    puts("/-------------------------------\\");
    puts("-*-*-*-*- Gifts Manager -*-*-*-*-");
    puts("\\-------------------------------/");
    
    for (;;) {
        menu();
        int choice = read_int();
        
        switch (choice) {
            case 1:
                make_gift();
                break;
            case 2:
                check_gift();
                break;
            case 3:
                send_gift();
                break;
            case 4:
                puts("Goodbye!");
                exit(0);
            default:
                puts("Invalid choice!");
        }
    }
    
    return 0;
}
