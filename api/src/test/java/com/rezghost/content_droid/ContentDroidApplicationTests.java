package com.rezghost.content_droid;

import org.junit.jupiter.api.Test;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.bean.override.mockito.MockitoBean;

import com.rezghost.content_droid.services.GenerationService;

@SpringBootTest
class ContentDroidApplicationTests {
	@MockitoBean
	GenerationService generationService;

	@Test
	void contextLoads() {
	}

}
