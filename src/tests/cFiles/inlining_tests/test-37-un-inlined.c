#include <assert.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#define MAX_CHARACTERS 1005
#define MAX_PARAGRAPHS 5

struct word {
  char* data;
};

struct sentence {
  struct word* data;
  int word_count;  // denotes number of words in a sentence
};

struct paragraph {
  struct sentence* data;
  int sentence_count;  // denotes number of sentences in a paragraph
};

struct document {
  struct paragraph* data;
  int paragraph_count;  // denotes number of paragraphs in a document
};

struct document get_document(char* text) {
  struct document doc;

  int pcount = 0;
  for (int i = 0; i < strlen(text); i++) {
    if (text[i] == '\n') pcount++;
  }
  pcount++;

  doc.paragraph_count = pcount;
  doc.data = malloc(pcount * sizeof(struct paragraph));

  for (int n = 0, m = 0, l = 0, i = 0; i < pcount; i++) {
    int scount = 0;
    while (text[n] != '\n' && n < strlen(text)) {
      if (text[n] == '.') scount++;
      n++;
    }
    n++;

    doc.data[i].sentence_count = scount;
    doc.data[i].data = malloc(scount * sizeof(struct sentence));

    for (int j = 0; j < scount; j++) {
      int wcount = 0;
      while (text[m] != '.' && m < n) {
        if (text[m] == ' ') wcount++;
        m++;
      }
      m++;
      if (text[m] == '\n') m++;
      wcount++;

      doc.data[i].data[j].word_count = wcount;
      doc.data[i].data[j].data = malloc(wcount * sizeof(struct word));

      for (int k = 0; k < wcount; k++) {
        int ccount = 0;
        while (text[l] != ' ' && text[l] != '.' && l < m) {
          ccount++;
          l++;
        }
        l++;
        if (text[l] == '\n') l++;

        ccount++;
        doc.data[i].data[j].data[k].data = malloc(ccount * sizeof(char));
      }
    }
  }

  int r = 0;
  for (int i = 0; i < doc.paragraph_count; i++) {
    for (int j = 0; j < doc.data[i].sentence_count; j++) {
      for (int k = 0; k < doc.data[i].data[j].word_count; k++) {
        int l = 0;
        while (text[r] != ' ' && text[r] != '.' && text[r] != '\n') {
          doc.data[i].data[j].data[k].data[l] = text[r];
          r++;
          l++;
        }
        doc.data[i].data[j].data[k].data[l] = '\0';
        if (text[r] == '.') {
          r++;
          break;
        }
        r++;
      }
      if (text[r] == '\n') {
        r++;
        break;
      }
    }
  }

  return doc;
}

struct word kth_word_in_mth_sentence_of_nth_paragraph(struct document Doc,
                                                      int k, int m, int n) {
  return Doc.data[n - 1].data[m - 1].data[k - 1];
}

struct sentence kth_sentence_in_mth_paragraph(struct document Doc, int k,
                                              int m) {
  return Doc.data[m - 1].data[k - 1];
}

struct paragraph kth_paragraph(struct document Doc, int k) {
  return Doc.data[k - 1];
}

void print_word(struct word w) { printf("%s", w.data); }

void print_sentence(struct sentence sen) {
  for (int i = 0; i < sen.word_count; i++) {
    print_word(sen.data[i]);
    if (i != sen.word_count - 1) {
      printf(" ");
    }
  }
}

void print_paragraph(struct paragraph para) {
  for (int i = 0; i < para.sentence_count; i++) {
    print_sentence(para.data[i]);
    printf(".");
  }
}

void print_document(struct document doc) {
  for (int i = 0; i < doc.paragraph_count; i++) {
    print_paragraph(doc.data[i]);
    if (i != doc.paragraph_count - 1) printf("\n");
  }
}

char* get_input_text() {
  int paragraph_count;
  scanf("%d", &paragraph_count);

  char p[MAX_PARAGRAPHS][MAX_CHARACTERS], doc[MAX_CHARACTERS];
  memset(doc, 0, sizeof(doc));
  getchar();
  for (int i = 0; i < paragraph_count; i++) {
    scanf("%[^\n]%*c", p[i]);
    strcat(doc, p[i]);
    if (i != paragraph_count - 1) strcat(doc, "\n");
  }

  char* returnDoc = (char*)malloc((strlen(doc) + 1) * (sizeof(char)));
  strcpy(returnDoc, doc);
  return returnDoc;
}

int main() {
  char* text = get_input_text();
  struct document Doc = get_document(text);

  int q;
  scanf("%d", &q);

  while (q--) {
    int type;
    scanf("%d", &type);

    if (type == 3) {
      int k, m, n;
      scanf("%d %d %d", &k, &m, &n);
      struct word w = kth_word_in_mth_sentence_of_nth_paragraph(Doc, k, m, n);
      print_word(w);
    }

    else if (type == 2) {
      int k, m;
      scanf("%d %d", &k, &m);
      struct sentence sen = kth_sentence_in_mth_paragraph(Doc, k, m);
      print_sentence(sen);
    }

    else {
      int k;
      scanf("%d", &k);
      struct paragraph para = kth_paragraph(Doc, k);
      print_paragraph(para);
    }
    printf("\n");
  }
}