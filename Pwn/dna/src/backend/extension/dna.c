#include <string.h>
#include <stdlib.h>
#include <stdint.h>
#include <stdio.h>

#define MAX_BUF 64
#define XOR_KEY 0x7A
#define TARGET_ROLE 0x1337C0DE

typedef struct {
    char username[MAX_BUF];
    uint32_t check_val;
    volatile int role;
} Session;

int _hex_decode(const char* input, uint8_t* output, int max_len) {
    int len = 0;
    while(input[0] && input[1] && len < max_len) {
        sscanf(input, "%2hhx", &output[len]);
        input += 2;
        len++;
    }
    return len;
}

void _decrypt(uint8_t* buffer, int len) {
    for(int i = 0; i < len; i++) buffer[i] ^= XOR_KEY;
}

uint16_t _calc_checksum(uint8_t* buffer, int len) {
    uint16_t sum = 0xAAAA;
    for(int i = 0; i < len; i++) {
        sum ^= buffer[i];
        if (sum & 1) sum = (sum >> 1) ^ 0x8008;
        else sum >>= 1;
    }
    return sum;
}

int dna_process_packet(const char* hex_input) {
    Session sess;
    memset(&sess, 0, sizeof(Session));
    sess.role = 0;

    uint8_t raw[256];
    uint8_t payload[256];

    int total_len = _hex_decode(hex_input, raw, 256);
    if (total_len < 3) return 0;

    uint8_t declared_len = raw[0];
    uint16_t declared_sum = (raw[1] << 8) | raw[2];

    if (declared_len > total_len - 3) return 0;

    memcpy(payload, raw + 3, declared_len);
    _decrypt(payload, declared_len);

    uint16_t real_sum = _calc_checksum(payload, declared_len);
    if (real_sum != declared_sum) return 0;

    memcpy(sess.username, payload, declared_len);

    if (sess.role == TARGET_ROLE) {
        return TARGET_ROLE;
    }

    return sess.role;
}
