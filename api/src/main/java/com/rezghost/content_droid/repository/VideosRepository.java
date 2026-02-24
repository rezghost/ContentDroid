package com.rezghost.content_droid.repository;

import java.util.UUID;
import org.springframework.data.repository.CrudRepository;
import com.rezghost.content_droid.models.VideoEntity;

public interface VideosRepository extends CrudRepository<VideoEntity, UUID> {
}
